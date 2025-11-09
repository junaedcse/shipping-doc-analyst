"""Tests for logging module."""
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, parent_dir)

import pytest
from shipping_doc_analyst.utils.logger import setup_logger, log

def test_logger_setup():
    """Test logger configuration."""
    setup_logger(log_level="DEBUG")
    assert log is not None
    
def test_logger_levels():
    """Test different log levels."""
    setup_logger(log_level="INFO")
    log.info("Test info message")
    log.warning("Test warning message")
    log.error("Test error message")
    # Should not raise any errors
