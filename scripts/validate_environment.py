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
