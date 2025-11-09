"""Tests for custom exceptions."""
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, parent_dir)

import pytest
from shipping_doc_analyst.utils.exceptions import (
    ShippingDocAnalystError,
    DocumentProcessingError,
    ValidationError,
)

def test_base_exception():
    """Test base exception."""
    with pytest.raises(ShippingDocAnalystError):
        raise ShippingDocAnalystError("Test error")

def test_document_processing_error():
    """Test document processing exception."""
    with pytest.raises(DocumentProcessingError):
        raise DocumentProcessingError("Processing failed")

def test_validation_error():
    """Test validation exception."""
    with pytest.raises(ValidationError):
        raise ValidationError("Validation failed")
