class DocumentProcessingError(Exception):
    """Raised when document processing fails at any stage (parsing, chunking, etc.)"""
    def __init__(self, filename: str, reason: str):
        super().__init__(f"Failed to process {filename}: {reason}")
        self.filename = filename
        self.reason = reason

class VectorizationError(Exception):
    """Raised when vector embedding generation or storage fails"""
    def __init__(self, doc_id: str, reason: str):
        super().__init__(f"Vectorization failed for document {doc_id}: {reason}")
        self.doc_id = doc_id
        self.reason = reason

class LLMError(Exception):
    """Raised when LLM interaction fails"""
    def __init__(self, query: str, reason: str):
        super().__init__(f"LLM failed to process query '{query[:20]}...': {reason}")
        self.query = query
        self.reason = reason