# LAYER -1: MANUAL SETUP COMMANDS
# Copy and paste these commands one section at a time

# ============================================================
# SECTION 1: Initial Setup
# ============================================================

# Navigate to your projects directory
cd ~/projects  # or wherever you want to create the project

# Create and enter project directory
mkdir shipping-doc-analyst
cd shipping-doc-analyst

# Initialize Git
git init

# ============================================================
# SECTION 2: Create .gitignore
# ============================================================

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Environment Variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data Files
data/raw/**/*.pdf
data/processed/**/*.pdf
data/faiss_index/

!data/raw/.gitkeep
!data/processed/.gitkeep
!data/ground_truth/.gitkeep
!data/faiss_index/.gitkeep

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# MyPy
.mypy_cache/

.DS_Store
Thumbs.db
EOF

# ============================================================
# SECTION 3: Create Directory Structure
# ============================================================

# Create data directories
mkdir -p data/raw/invoices
mkdir -p data/raw/purchase_orders
mkdir -p data/raw/shipping_orders
mkdir -p data/processed
mkdir -p data/ground_truth/train
mkdir -p data/ground_truth/validation
mkdir -p data/ground_truth/test
mkdir -p data/faiss_index

# Create other directories
mkdir -p docs
mkdir -p notebooks
mkdir -p scripts

# Create package directories
mkdir -p shipping_doc_analyst/config
mkdir -p shipping_doc_analyst/core
mkdir -p shipping_doc_analyst/agents
mkdir -p shipping_doc_analyst/integrations
mkdir -p shipping_doc_analyst/pipelines
mkdir -p shipping_doc_analyst/evaluation
mkdir -p shipping_doc_analyst/utils
mkdir -p shipping_doc_analyst/cli

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures/sample_docs

# Create .gitkeep files
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/ground_truth/.gitkeep
touch data/faiss_index/.gitkeep

# ============================================================
# SECTION 4: Create __init__.py Files
# ============================================================

touch shipping_doc_analyst/__init__.py
touch shipping_doc_analyst/config/__init__.py
touch shipping_doc_analyst/core/__init__.py
touch shipping_doc_analyst/agents/__init__.py
touch shipping_doc_analyst/integrations/__init__.py
touch shipping_doc_analyst/pipelines/__init__.py
touch shipping_doc_analyst/evaluation/__init__.py
touch shipping_doc_analyst/utils/__init__.py
touch shipping_doc_analyst/cli/__init__.py
touch tests/__init__.py

# ============================================================
# SECTION 5: Create Virtual Environment
# ============================================================

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
# On Windows use: .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip wheel setuptools

# ============================================================
# SECTION 6: Create requirements.txt
# ============================================================

cat > requirements.txt << 'EOF'
# LLM and Orchestration
langchain==0.1.0
langgraph==0.0.26
openai==1.12.0

# Vector Store
faiss-cpu==1.7.4

# Document Processing
pypdf2==3.0.1
pdfplumber==0.10.3
pillow==10.2.0

# Google Drive Integration
google-api-python-client==2.118.0
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0

# Data Handling
pandas==2.1.4
numpy==1.26.3
pydantic==2.5.3
pydantic-settings==2.1.0

# Evaluation
scikit-learn==1.4.0

# Utilities
python-dotenv==1.0.1
tqdm==4.66.1
rich==13.7.0
click==8.1.7

# Logging
loguru==0.7.2
EOF

# ============================================================
# SECTION 7: Create requirements-dev.txt
# ============================================================

cat > requirements-dev.txt << 'EOF'
# Include production requirements
-r requirements.txt

# Testing
pytest==7.4.4
pytest-cov==4.1.0
pytest-mock==3.12.0

# Code Quality
black==24.1.1
isort==5.13.2
pylint==3.0.3
mypy==1.8.0
flake8==7.0.0

# Type Stubs
types-requests==2.31.0.20240125

# Jupyter
jupyter==1.0.0
ipykernel==6.29.0

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0
EOF

# ============================================================
# SECTION 8: Install Dependencies (2-5 minutes)
# ============================================================

pip install -r requirements-dev.txt

# Verify installations
python -c "import langchain; print('LangChain OK')"
python -c "import faiss; print('FAISS OK')"
python -c "import openai; print('OpenAI OK')"

# ============================================================
# SECTION 9: Create Configuration Files
# ============================================================

# Create .env.example
cat > .env.example << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Google Drive Configuration
GOOGLE_DRIVE_CREDENTIALS_PATH=./credentials/google_credentials.json
GOOGLE_DRIVE_INPUT_FOLDER_ID=your_folder_id_here
GOOGLE_DRIVE_OUTPUT_FOLDER_ID=your_folder_id_here

# FAISS Configuration
FAISS_INDEX_PATH=./data/faiss_index
FAISS_INDEX_TYPE=IndexFlatIP

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Processing Configuration
BATCH_SIZE=10
MAX_WORKERS=4
PROCESSING_TIMEOUT=120

# Evaluation Configuration
CONFIDENCE_THRESHOLD=0.7
SIMILARITY_THRESHOLD=0.8
EOF

# Copy to actual .env
cp .env.example .env

# IMPORTANT: Now edit .env and add your OpenAI API key
# Use: nano .env  or  code .env  or your preferred editor

# ============================================================
# SECTION 10: Create README.md
# ============================================================

cat > README.md << 'EOF'
# Intelligent Shipping Document Analyst

AI-powered document processing system for shipping documents using RAG (Retrieval-Augmented Generation) and agentic workflows.

## Features

- 🤖 Automated entity extraction from shipping documents
- 🔍 Semantic search across historical documents using FAISS
- ✅ Intelligent validation and anomaly detection
- 📊 Comprehensive evaluation framework with F1 metrics
- 🔄 LangGraph-powered agentic workflow
- ☁️ Google Drive integration for document management

## Document Types Supported

- Invoices
- Purchase Orders
- Shipping Orders
- Bills of Lading
- Packing Lists
- Commercial Invoices

## Technology Stack

- **Language:** Python 3.10+
- **LLM:** OpenAI GPT-4
- **Framework:** LangChain + LangGraph
- **Vector Store:** FAISS
- **Document Processing:** PyPDF2, pdfplumber
- **Cloud:** Google Drive API

## Current Status

- [x] Layer -1: Project Foundation ✓
- [ ] Layer 0: Data Preparation (Next)
- [ ] Layer 1: Data Ingestion
- [ ] Layer 2: Document Processing
- [ ] Layer 3: Vector Store
- [ ] Layer 4: Agentic Workflow
- [ ] Layer 5: Output & Evaluation

## License

MIT License
EOF

# ============================================================
# SECTION 11: Create setup.py
# ============================================================

cat > setup.py << 'EOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shipping-doc-analyst",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered shipping document analysis system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shipping-analyst=shipping_doc_analyst.cli.main:cli",
        ],
    },
)
EOF

# ============================================================
# SECTION 12: Create pyproject.toml
# ============================================================

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "shipping-doc-analyst"
version = "0.1.0"
description = "AI-powered shipping document analysis system"
readme = "README.md"
requires-python = ">=3.10"

[tool.black]
line-length = 100
target-version = ['py310']

[tool.isort]
profile = "black"
line_length = 100

[tool.pylint.main]
max-line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=shipping_doc_analyst"

[tool.mypy]
python_version = "3.10"
ignore_missing_imports = true
EOF

# Install package in editable mode
pip install -e .

# ============================================================
# SECTION 13: Create Utility Modules
# ============================================================

# Create logger.py
cat > shipping_doc_analyst/utils/logger.py << 'EOF'
"""Logging configuration for the application."""
import sys
from pathlib import Path
from loguru import logger

def setup_logger(log_level: str = "INFO", log_file: str | None = None) -> None:
    """Configure logger with console and file handlers."""
    logger.remove()
    
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
        )
    
    logger.info(f"Logger configured with level: {log_level}")

log = logger
EOF

# Create exceptions.py
cat > shipping_doc_analyst/utils/exceptions.py << 'EOF'
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
EOF

# Create settings.py
cat > shipping_doc_analyst/config/settings.py << 'EOF'
"""Application configuration management."""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-large", 
        env="OPENAI_EMBEDDING_MODEL"
    )
    
    google_drive_credentials_path: str | None = Field(
        default=None, env="GOOGLE_DRIVE_CREDENTIALS_PATH"
    )
    google_drive_input_folder_id: str | None = Field(
        default=None, env="GOOGLE_DRIVE_INPUT_FOLDER_ID"
    )
    google_drive_output_folder_id: str | None = Field(
        default=None, env="GOOGLE_DRIVE_OUTPUT_FOLDER_ID"
    )
    
    faiss_index_path: Path = Field(
        default=Path("./data/faiss_index"), env="FAISS_INDEX_PATH"
    )
    faiss_index_type: str = Field(default="IndexFlatIP", env="FAISS_INDEX_TYPE")
    
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str | None = Field(default="./logs/app.log", env="LOG_FILE")
    
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    processing_timeout: int = Field(default=120, env="PROCESSING_TIMEOUT")
    
    confidence_threshold: float = Field(default=0.7, env="CONFIDENCE_THRESHOLD")
    similarity_threshold: float = Field(default=0.8, env="SIMILARITY_THRESHOLD")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
EOF

# Test imports
python -c "from shipping_doc_analyst.utils.logger import setup_logger, log; print('Logger OK')"
python -c "from shipping_doc_analyst.utils.exceptions import DocumentProcessingError; print('Exceptions OK')"
python -c "from shipping_doc_analyst.config.settings import settings; print('Settings OK')"

# ============================================================
# SECTION 14: Create Test Files
# ============================================================

# Test config
cat > tests/unit/test_config.py << 'EOF'
"""Tests for configuration module."""
import pytest
from shipping_doc_analyst.config.settings import Settings

def test_settings_default_values():
    """Test that settings have default values."""
    settings = Settings(openai_api_key="test-key")
    assert settings.openai_model == "gpt-4"
    assert settings.batch_size == 10
    assert settings.log_level == "INFO"
EOF

# Test logger
cat > tests/unit/test_logger.py << 'EOF'
"""Tests for logging module."""
from shipping_doc_analyst.utils.logger import setup_logger, log

def test_logger_setup():
    """Test logger configuration."""
    setup_logger(log_level="DEBUG")
    assert log is not None
EOF

# Test exceptions
cat > tests/unit/test_exceptions.py << 'EOF'
"""Tests for custom exceptions."""
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
EOF

# Run tests
pytest tests/unit/ -v

# ============================================================
# SECTION 15: Create Validation Script
# ============================================================

cat > scripts/validate_environment.py << 'EOF'
"""Validate that the environment is set up correctly."""
import sys
from pathlib import Path

def validate_environment():
    """Run validation checks on the environment."""
    print("=" * 60)
    print("ENVIRONMENT VALIDATION")
    print("=" * 60)
    
    checks_passed = 0
    checks_failed = 0
    
    # Check Python version
    print("\n[1] Checking Python version...")
    if sys.version_info >= (3, 10):
        print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}")
        checks_passed += 1
    else:
        print(f"   ✗ Python {sys.version_info}")
        checks_failed += 1
    
    # Check packages
    print("\n[2] Checking required packages...")
    packages = ["langchain", "langgraph", "openai", "faiss", "pypdf2", "pdfplumber", "pandas", "pydantic", "pytest", "loguru"]
    
    for package in packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
            checks_passed += 1
        except ImportError:
            print(f"   ✗ {package}")
            checks_failed += 1
    
    # Check structure
    print("\n[3] Checking project structure...")
    dirs = ["data/raw", "data/ground_truth", "shipping_doc_analyst/config", "tests/unit"]
    
    for dir_path in dirs:
        if Path(dir_path).exists():
            print(f"   ✓ {dir_path}/")
            checks_passed += 1
        else:
            print(f"   ✗ {dir_path}/")
            checks_failed += 1
    
    # Check config files
    print("\n[4] Checking configuration files...")
    files = [".env", "requirements.txt", "setup.py", "README.md"]
    
    for file_path in files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
            checks_passed += 1
        else:
            print(f"   ✗ {file_path}")
            checks_failed += 1
    
    # Check environment variables
    print("\n[5] Checking environment variables...")
    try:
        from shipping_doc_analyst.config.settings import settings
        
        if settings.openai_api_key != "your_openai_api_key_here":
            print(f"   ✓ OPENAI_API_KEY configured")
            checks_passed += 1
        else:
            print(f"   ⚠ OPENAI_API_KEY not configured - please edit .env")
        
        print(f"   ✓ Log level: {settings.log_level}")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ Error: {e}")
        checks_failed += 1
    
    # Check PDFs
    print("\n[6] Checking for PDF documents...")
    pdf_count = len(list(Path("data/raw").rglob("*.pdf")))
    print(f"   Found {pdf_count} PDFs")
    if pdf_count == 0:
        print(f"   ⚠ No PDFs found - copy your documents to data/raw/")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Passed: {checks_passed}")
    print(f"Failed: {checks_failed}")
    
    if checks_failed == 0:
        print("\n✓ Environment is ready!")
        print("\nNext steps:")
        print("1. Edit .env and add your OpenAI API key")
        print("2. Copy PDFs to data/raw/ subdirectories")
        print("3. Proceed to Layer 0")
        return True
    else:
        print(f"\n✗ Fix {checks_failed} issues")
        return False

if __name__ == "__main__":
    validate_environment()
EOF

# Run validation
python scripts/validate_environment.py

# ============================================================
# SECTION 16: Commit to Git
# ============================================================

git add .
git commit -m "Initial project setup - Layer -1 complete"

# ============================================================
# COMPLETION MESSAGE
# ============================================================

echo ""
echo "============================================================"
echo "✓ LAYER -1 SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. Copy your PDF documents to:"
echo "   data/raw/invoices/"
echo "   data/raw/purchase_orders/"
echo "   data/raw/shipping_orders/"
echo ""
echo "3. Verify everything:"
echo "   python scripts/validate_environment.py"
echo ""
echo "4. Proceed to Layer 0 (Data Preparation)"
echo ""
