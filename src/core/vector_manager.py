import time
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http import exceptions as qdrant_exceptions
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from src.config.settings import EmbeddingModels, VectorConfig
from uuid import uuid5, NAMESPACE_URL
import numpy as np
import logging

logger = logging.getLogger(__name__)

class VectorManager:
    def __init__(self, model_name: str = EmbeddingModels.SENTENCE_BERT.value):
        self.client = QdrantClient(
                            host=VectorConfig.QDRANT_LOCATION.split(":")[0],
                            port=int(VectorConfig.QDRANT_LOCATION.split(":")[1]),
                            prefer_grpc=True
                      )
        self.embedding_model = self._init_model(model_name)
        self._init_collection()

    def _connect_with_retry(self, max_retries=5, delay=5):
        for attempt in range(max_retries):
            try:
                client = QdrantClient(
                    host=VectorConfig.QDRANT_HOST,
                    port=VectorConfig.QDRANT_PORT
                )
                client.get_collections()  # Test connection
                return client
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Connection failed, retrying in {delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)

    def _init_model(self, model_name: str):
        """Initialize embedding model based on config"""
        if "sentence-transformers" in model_name:
            return SentenceTransformer(model_name)
        elif "text-embedding" in model_name:
            return "openai"
        elif "BAAI" in model_name:
            return "bge"
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def _init_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collection_info = self.client.get_collection(VectorConfig.COLLECTION_NAME)
            if collection_info.vectors_count == 0:
                self._create_collection()
        except Exception:
           self._create_collection()

    def _create_collection(self):
        self.client.recreate_collection(
            collection_name = VectorConfig.COLLECTION_NAME,
            vectors_config = models.VectorParams(
                size = self._get_embedding_size(),
                distance = models.Distance.COSINE
            ),
            timeout=60
        )

    def _get_embedding_size(self) -> int:
        """Get vector dimensions based on model"""
        if isinstance(self.embedding_model, SentenceTransformer):
            return self.embedding_model.get_sentence_embedding_dimension()
        elif self.embedding_model == "openai":
            return 1536  # ADA-002 dimension
        elif self.embedding_model == "bge":
            return 768
        return 768  # default

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Convert text chunks to embeddings"""
        try:
            if isinstance(self.embedding_model, SentenceTransformer):
                return self.embedding_model.encode(texts).tolist()
        # Add implementations for other models here
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")

    def store_embeddings(self, doc_id: str, chunks: list[str], embeddings: list[list[float]]):
        """Store embeddings in Qdrant with document metadata"""
        try:
            points = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                unique_id = str(uuid5(NAMESPACE_URL, f"{doc_id}_{idx}"))
                points.append(
                    PointStruct(
                        id=unique_id,
                        vector=embedding,
                        payload={
                            "doc_id": doc_id,
                            "chunk_text": chunk,
                            "chunk_index": idx
                        }
                    )
                )

        except Exception as e:
            logger.error(f"failed to Store embeddings: {str(e)}")
            raise

        # Batch upload
        for i in range(0, len(points), VectorConfig.BATCH_SIZE):
            batch = points[i:i+VectorConfig.BATCH_SIZE]
            self.client.upsert(
                collection_name=VectorConfig.COLLECTION_NAME,
                points=batch
            )
