"""Tests for configuration module."""
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, parent_dir)

import pytest
from shipping_doc_analyst.config.settings import Settings

def test_settings_default_values():
    """Test that settings have default values."""
    settings = Settings(openai_api_key="test-key")
    assert settings.openai_model == "gpt-4"
    assert settings.batch_size == 10
    assert settings.log_level == "INFO"

def test_settings_with_custom_values():
    """Test settings with custom environment variables."""
    custom_settings = Settings(
        openai_api_key="test-key",
        batch_size=20,
        log_level="DEBUG"
    )
    assert custom_settings.batch_size == 20
    assert custom_settings.log_level == "DEBUG"
