"""Custom exceptions for the application."""

class ShippingDocAnalystError(Exception):
    """Base exception for all application errors."""
    pass

class DocumentProcessingError(ShippingDocAnalystError):
    """Raised when document processing fails."""
    pass

class EmbeddingGenerationError(ShippingDocAnalystError):
    """Raised when embedding generation fails."""
    pass

class VectorStoreError(ShippingDocAnalystError):
    """Raised when vector store operations fail."""
    pass

class APIConnectionError(ShippingDocAnalystError):
    """Raised when API connection fails."""
    pass

class ValidationError(ShippingDocAnalystError):
    """Raised when validation fails."""
    pass

class ConfigurationError(ShippingDocAnalystError):
    """Raised when configuration is invalid."""
    pass
