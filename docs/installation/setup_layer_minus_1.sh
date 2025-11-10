#!/bin/bash

# ============================================================
# LAYER -1: PROJECT FOUNDATION SETUP SCRIPT
# ============================================================
# This script automates the complete setup of the project
# foundation including directory structure, virtual environment,
# dependencies, and configuration files.
#
# Usage: bash setup_layer_minus_1.sh
# ============================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Progress tracker
STEP=0
TOTAL_STEPS=21

print_header() {
    echo ""
    echo "============================================================"
    echo -e "${BLUE}$1${NC}"
    echo "============================================================"
    echo ""
}

print_step() {
    STEP=$((STEP + 1))
    echo ""
    echo -e "${GREEN}[STEP $STEP/$TOTAL_STEPS]${NC} $1"
    echo "------------------------------------------------------------"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Python 3.10+ is available
check_python_version() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        REQUIRED_VERSION="3.10"
        
        if awk "BEGIN {exit !($PYTHON_VERSION >= $REQUIRED_VERSION)}"; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python $PYTHON_VERSION is too old. Need 3.10+"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.10+"
        return 1
    fi
}

# ============================================================
# MAIN SETUP PROCESS
# ============================================================

print_header "LAYER -1: PROJECT FOUNDATION SETUP"

echo "This script will create a complete project structure for"
echo "Intelligent Shipping Document Analyst system."
echo ""
echo "Current directory: $(pwd)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

# Check Python version
print_step "Checking Python version"
if ! check_python_version; then
    exit 1
fi

# STEP 1: Create project directory
print_step "Creating project directory"
PROJECT_NAME="shipping-doc-analyst"

if [ -d "$PROJECT_NAME" ]; then
    print_warning "Directory $PROJECT_NAME already exists"
    read -p "Continue and potentially overwrite files? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
else
    mkdir -p "$PROJECT_NAME"
    print_success "Created directory: $PROJECT_NAME"
fi

cd "$PROJECT_NAME"
print_success "Working directory: $(pwd)"

# STEP 2: Initialize Git repository
print_step "Initializing Git repository"
if [ ! -d ".git" ]; then
    git init
    print_success "Git repository initialized"
else
    print_warning "Git repository already exists"
fi

# STEP 3: Create .gitignore
print_step "Creating .gitignore"
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

# Data Files (too large for git)
data/raw/**/*.pdf
data/processed/**/*.pdf
data/faiss_index/

# But keep data directory structure
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

# Mac
.DS_Store

# Windows
Thumbs.db
EOF
print_success "Created .gitignore"

# STEP 4: Create directory structure
print_step "Creating complete directory structure"

# Data directories
mkdir -p data/raw/invoices
mkdir -p data/raw/purchase_orders
mkdir -p data/raw/shipping_orders
mkdir -p data/processed
mkdir -p data/ground_truth/train
mkdir -p data/ground_truth/validation
mkdir -p data/ground_truth/test
mkdir -p data/faiss_index

# Documentation
mkdir -p docs

# Notebooks
mkdir -p notebooks

# Scripts
mkdir -p scripts

# Main package
mkdir -p shipping_doc_analyst/config
mkdir -p shipping_doc_analyst/core
mkdir -p shipping_doc_analyst/agents
mkdir -p shipping_doc_analyst/integrations
mkdir -p shipping_doc_analyst/pipelines
mkdir -p shipping_doc_analyst/evaluation
mkdir -p shipping_doc_analyst/utils
mkdir -p shipping_doc_analyst/cli

# Tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures/sample_docs

# Create .gitkeep files
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/ground_truth/.gitkeep
touch data/faiss_index/.gitkeep

print_success "Directory structure created"

# STEP 5: Create __init__.py files
print_step "Creating Python package __init__.py files"

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

print_success "Created __init__.py files"

# STEP 6: Create virtual environment
print_step "Creating virtual environment (.venv)"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_success "Activating virtual environment..."
source .venv/bin/activate

# STEP 7: Upgrade pip
print_step "Upgrading pip and core tools"

pip install --upgrade pip wheel setuptools
print_success "pip, wheel, and setuptools upgraded"

# STEP 8: Create requirements.txt
print_step "Creating requirements.txt"

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
print_success "Created requirements.txt"

# STEP 9: Create requirements-dev.txt
print_step "Creating requirements-dev.txt"

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
print_success "Created requirements-dev.txt"

# STEP 10: Install dependencies
print_step "Installing dependencies (this may take 2-5 minutes)"

pip install -r requirements-dev.txt
print_success "All dependencies installed"

# STEP 11: Create .env.example
print_step "Creating .env.example template"

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
print_success "Created .env.example"

# STEP 12: Create .env file
print_step "Creating .env file"

cp .env.example .env
print_success "Created .env (you need to add your OpenAI API key)"
print_warning "IMPORTANT: Edit .env and add your OpenAI API key!"

# STEP 13: Create README.md
print_step "Creating README.md"

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

## Project Structure

```
shipping-doc-analyst/
├── data/                   # Data files (not in git)
├── shipping_doc_analyst/   # Main package
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── notebooks/              # Jupyter notebooks
```

## Setup

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Google Drive API credentials (optional)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd shipping-doc-analyst
```

2. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Copy your PDF documents:
```bash
# Place your PDFs in data/raw/
cp /path/to/your/pdfs/*.pdf data/raw/invoices/
```

## Usage

### 1. Prepare Data (Layer 0)
```bash
python scripts/annotate_documents.py --input data/raw/ --output data/ground_truth/
```

### 2. Build FAISS Index
```bash
python -m shipping_doc_analyst.cli index --data-dir data/ground_truth/train/
```

### 3. Process Documents
```bash
python -m shipping_doc_analyst.cli process --input data/raw/invoices/
```

### 4. Run Evaluation
```bash
python -m shipping_doc_analyst.cli evaluate --test-dir data/ground_truth/test/
```

## Development

### Running Tests
```bash
pytest tests/ -v --cov=shipping_doc_analyst
```

### Code Quality
```bash
# Format code
black shipping_doc_analyst/ tests/

# Sort imports
isort shipping_doc_analyst/ tests/

# Lint
pylint shipping_doc_analyst/

# Type checking
mypy shipping_doc_analyst/
```

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

## Author

Your Name

## Acknowledgments

- OpenAI for GPT-4 API
- LangChain/LangGraph team
- Facebook AI for FAISS
EOF
print_success "Created README.md"

# STEP 14: Create setup.py
print_step "Creating setup.py"

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
    url="https://github.com/yourusername/shipping-doc-analyst",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
print_success "Created setup.py"

# STEP 15: Create pyproject.toml
print_step "Creating pyproject.toml"

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
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["ai", "document-processing", "shipping", "rag", "langchain"]

[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
skip_gitignore = true

[tool.pylint.main]
max-line-length = 100
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring  
    "C0116",  # missing-function-docstring
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=shipping_doc_analyst --cov-report=html --cov-report=term"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
EOF
print_success "Created pyproject.toml"

# STEP 16: Install package in editable mode
print_step "Installing package in editable mode"

pip install -e .
print_success "Package installed"

# STEP 17: Create utility modules
print_step "Creating utility modules"

# Logger
cat > shipping_doc_analyst/utils/logger.py << 'EOF'
"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from loguru import logger

def setup_logger(log_level: str = "INFO", log_file: str | None = None) -> None:
    """Configure logger with console and file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    
    # Add file handler if specified
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

# Create a module-level logger instance
log = logger
EOF

# Exceptions
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

# Settings
cat > shipping_doc_analyst/config/settings.py << 'EOF'
"""Application configuration management."""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-large", 
        env="OPENAI_EMBEDDING_MODEL"
    )
    
    # Google Drive Configuration
    google_drive_credentials_path: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_CREDENTIALS_PATH"
    )
    google_drive_input_folder_id: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_INPUT_FOLDER_ID"
    )
    google_drive_output_folder_id: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_OUTPUT_FOLDER_ID"
    )
    
    # FAISS Configuration
    faiss_index_path: Path = Field(
        default=Path("./data/faiss_index"),
        env="FAISS_INDEX_PATH"
    )
    faiss_index_type: str = Field(default="IndexFlatIP", env="FAISS_INDEX_TYPE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str | None = Field(default="./logs/app.log", env="LOG_FILE")
    
    # Processing Configuration
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    processing_timeout: int = Field(default=120, env="PROCESSING_TIMEOUT")
    
    # Evaluation Configuration
    confidence_threshold: float = Field(default=0.7, env="CONFIDENCE_THRESHOLD")
    similarity_threshold: float = Field(default=0.8, env="SIMILARITY_THRESHOLD")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()
EOF

print_success "Created utility modules"

# STEP 18: Create basic test files
print_step "Creating basic test files"

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

def test_settings_with_custom_values():
    """Test settings with custom environment variables."""
    custom_settings = Settings(
        openai_api_key="test-key",
        batch_size=20,
        log_level="DEBUG"
    )
    assert custom_settings.batch_size == 20
    assert custom_settings.log_level == "DEBUG"
EOF

# Test logger
cat > tests/unit/test_logger.py << 'EOF'
"""Tests for logging module."""
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

def test_document_processing_error():
    """Test document processing exception."""
    with pytest.raises(DocumentProcessingError):
        raise DocumentProcessingError("Processing failed")

def test_validation_error():
    """Test validation exception."""
    with pytest.raises(ValidationError):
        raise ValidationError("Validation failed")
EOF

print_success "Created test files"

# STEP 19: Run tests
print_step "Running tests"

pytest tests/unit/ -v
print_success "All tests passed"

# STEP 20: Create validation script
print_step "Creating environment validation script"

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
    
    # Check 1: Python version
    print("\n[1] Checking Python version...")
    if sys.version_info >= (3, 10):
        print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        checks_passed += 1
    else:
        print(f"   ✗ Python version too old: {sys.version_info}")
        checks_failed += 1
    
    # Check 2: Required packages
    print("\n[2] Checking required packages...")
    required_packages = [
        "langchain",
        "langgraph",
        "openai",
        "faiss",
        "pypdf2",
        "pdfplumber",
        "pandas",
        "pydantic",
        "pytest",
        "loguru",
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
            checks_passed += 1
        except ImportError:
            print(f"   ✗ {package} not installed")
            checks_failed += 1
    
    # Check 3: Project structure
    print("\n[3] Checking project structure...")
    required_dirs = [
        "data/raw",
        "data/ground_truth",
        "data/faiss_index",
        "shipping_doc_analyst/config",
        "shipping_doc_analyst/core",
        "shipping_doc_analyst/utils",
        "tests/unit",
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✓ {dir_path}/")
            checks_passed += 1
        else:
            print(f"   ✗ {dir_path}/ missing")
            checks_failed += 1
    
    # Check 4: Configuration files
    print("\n[4] Checking configuration files...")
    config_files = [
        ".env",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "README.md",
    ]
    
    for file_path in config_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
            checks_passed += 1
        else:
            print(f"   ✗ {file_path} missing")
            checks_failed += 1
    
    # Check 5: Environment variables
    print("\n[5] Checking environment variables...")
    try:
        from shipping_doc_analyst.config.settings import settings
        
        if settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here":
            print(f"   ✓ OPENAI_API_KEY configured")
            checks_passed += 1
        else:
            print(f"   ⚠ OPENAI_API_KEY not set or using default")
            print(f"     Please edit .env and add your OpenAI API key")
            # Don't fail, just warn
            
        print(f"   ✓ Log level: {settings.log_level}")
        checks_passed += 1
        
    except Exception as e:
        print(f"   ✗ Error loading settings: {e}")
        checks_failed += 1
    
    # Check 6: PDFs in data directory
    print("\n[6] Checking for PDF documents...")
    pdf_dirs = [
        "data/raw/invoices",
        "data/raw/purchase_orders",
        "data/raw/shipping_orders",
    ]
    
    total_pdfs = 0
    for pdf_dir in pdf_dirs:
        pdf_count = len(list(Path(pdf_dir).glob("*.pdf")))
        total_pdfs += pdf_count
        if pdf_count > 0:
            print(f"   ✓ {pdf_dir}: {pdf_count} PDFs")
            checks_passed += 1
        else:
            print(f"   ⚠ {pdf_dir}: No PDFs found (add your PDFs here)")
    
    print(f"\n   Total PDFs: {total_pdfs}")
    if total_pdfs == 0:
        print(f"   ⚠ No PDFs found. Copy your PDFs to data/raw/ subdirectories")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Checks passed: {checks_passed}")
    print(f"Checks failed: {checks_failed}")
    
    if checks_failed == 0:
        print("\n✓ Environment is properly configured!")
        print("✓ You can proceed to Layer 0 (Data Preparation)")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Copy your PDF documents to data/raw/ subdirectories")
        print("3. Run: python scripts/validate_environment.py")
        return True
    else:
        print(f"\n✗ Please fix {checks_failed} failed check(s) before proceeding")
        return False

if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)
EOF

print_success "Created validation script"

# STEP 21: Run validation
print_step "Running environment validation"

python scripts/validate_environment.py

# Final Git commit
print_step "Creating initial Git commit"

git add .
git commit -m "Initial project setup - Layer -1 complete

- Created complete project structure
- Set up virtual environment
- Installed all dependencies
- Created configuration files
- Added utility modules (logger, exceptions, settings)
- Added basic unit tests
- Validated environment setup
"

print_success "Git commit created"

# ============================================================
# COMPLETION
# ============================================================

print_header "LAYER -1 SETUP COMPLETE!"

echo -e "${GREEN}✓ Project foundation is ready!${NC}"
echo ""
echo "Directory: $(pwd)"
echo ""
echo -e "${YELLOW}IMPORTANT NEXT STEPS:${NC}"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Copy your PDF documents to data/raw/ subdirectories:"
echo "   - data/raw/invoices/"
echo "   - data/raw/purchase_orders/"
echo "   - data/raw/shipping_orders/"
echo "3. Verify setup:"
echo "   ${BLUE}python scripts/validate_environment.py${NC}"
echo ""
echo -e "${GREEN}Then proceed to Layer 0 (Data Preparation)${NC}"
echo ""
echo "To reactivate virtual environment in future sessions:"
echo "   ${BLUE}cd $(pwd)${NC}"
echo "   ${BLUE}source .venv/bin/activate${NC}"
echo ""
