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
