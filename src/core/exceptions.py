class DocumentProcessingError(Exception):
    """Raised when document processing fails"""
    def __init__(self, filename, reason):
        super().__init__(f"Failed to process {filename}: {reason}")

class VectorizationError(Exception):
    """Raised when vector operations fail"""

class LLMGenerationError(Exception):
    """Raised when LLM response generation fails"""
