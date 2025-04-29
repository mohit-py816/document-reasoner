import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class LLMModels(Enum):
    OPENAI_GPT4 = "gpt-4"
    OPENAI_GPT35 = "gpt-3.5-turbo"
    LLAMA2_7B = "llama-2-7b-chat"
    MISTRAL_7B = "mistral-7b-instruct"

class LLMConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "../../models")
    MAX_TOKENS = 10000
    TEMPERATURE = 0.7

class EmbeddingModels(Enum):
    SENTENCE_BERT = "sentence-transformers/all-mpnet-base-v2"
    OPENAI_ADA = "text-embedding-3-small"
    BGE_BASE = "BAAI/bge-base-en-v1.5"

class VectorConfig:
    QDRANT_LOCATION = "qdrant:6333"
    QDRANT_HOST = "qdrant"
    QDRANT_PORT = 6333
    COLLECTION_NAME = "document_embeddings"
    BATCH_SIZE = 32
    CHUNK_SIZE = 512  # characters
    CHUNK_OVERLAP = 50  # characters
