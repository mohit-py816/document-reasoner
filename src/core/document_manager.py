import logging
import hashlib
from pathlib import Path
from config.settings import VectorConfig
from core.document_parser import DocumentParser
from core.vector_manager import VectorManager
from core.chunking import TextChunker

logger = logging.getLogger(__name__)

class DocumentManager:
    def __init__(self):
        self.loaded_documents = {}  # {doc_id: {path: str, content: str, meta: dict}}
        self.vector_manager = VectorManager()
        self.chunking = TextChunker()

    def add_document(self, file_path: str) -> str:

        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            content = DocumentParser.parse(file_path)
            if not content:
                raise DocumentProcessingError(Path(file_path).name, "Empty content")

            """Process and store a document"""
            content = DocumentParser.parse(file_path)
            if not content:
                return None

            doc_id = self._generate_doc_id(file_path)
            chunks = self.chunking.chunk_text(content)
            embeddings = self.vector_manager.generate_embeddings(chunks)

            self.loaded_documents[doc_id] = {
                'path': file_path,
                'content': content,
                'chunks': chunks,
                'embeddings': embeddings,
                'meta': self._extract_metadata(file_path)
            }

            self.vector_manager.store_embeddings(doc_id, chunks, embeddings)
            return doc_id
        except Exception as e:
            logger.exception(f"Document processing failed")
            raise DocumentProcessingError(
                filename = Path(file_path).name,
                reason = str(e)
            ) from e


    def _generate_doc_id(self, file_path: str) -> str:
        """Create unique document ID from file contents"""
        file_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def _extract_metadata(self, file_path: str) -> dict:
        """Extract basic file metadata"""
        path = Path(file_path)
        return {
            'filename': path.name,
            'file_type': path.suffix[1:].upper(),
            'size': path.stat().st_size,
            'created': path.stat().st_ctime,
            'modified': path.stat().st_mtime
        }

    def get_document_content(self, doc_id: str) -> str:
        return self.loaded_documents.get(doc_id, {}).get('content', '')

    def retrieve_context(self, doc_id: str, query: str) -> str:
        """Retrieve relevant context chunks for a query"""
        vector_manager = VectorManager()
        query_embedding = vector_manager.generate_embeddings([query])[0]

        results = vector_manager.client.search(
            collection_name=VectorConfig.COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3,
            with_payload=True
        )
        return "\n".join([hit.payload["chunk_text"] for hit in results])
