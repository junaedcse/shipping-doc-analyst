#!/bin/bash

# ============================================================
# LAYER 0: DATA PREPARATION - EXECUTION GUIDE
# ============================================================
# Automates the data preparation workflow
# Run from project root: bash scripts/setup_layer_0.sh
# ============================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "============================================================"
echo -e "${BLUE}LAYER 0: DATA PREPARATION${NC}"
echo "============================================================"
echo ""

# Check we're in project root
if [ ! -f "setup.py" ]; then
    echo -e "${YELLOW}Error: Run this from project root directory${NC}"
    exit 1
fi

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Error: Virtual environment not found${NC}"
    echo "Run Layer -1 setup first"
    exit 1
fi

echo -e "${GREEN}[1/6]${NC} Activating virtual environment..."
source .venv/bin/activate

# Make scripts executable
echo -e "${GREEN}[2/6]${NC} Making scripts executable..."
chmod +x scripts/*.py

# Check for PDFs
echo ""
echo -e "${GREEN}[3/6]${NC} Checking for PDF documents..."
PDF_COUNT=$(find data/raw -name "*.pdf" 2>/dev/null | wc -l)

if [ $PDF_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠ No PDFs found in data/raw/${NC}"
    echo ""
    echo "Please copy your PDFs to:"
    echo "  data/raw/invoices/"
    echo "  data/raw/purchase_orders/"
    echo "  data/raw/shipping_orders/"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "  ✓ Found $PDF_COUNT PDF(s)"
fi

# Run document analysis
echo ""
echo -e "${GREEN}[4/6]${NC} Analyzing document structure..."
python scripts/analyze_documents.py

echo ""
echo "============================================================"
echo -e "${YELLOW}NEXT STEPS - MANUAL ANNOTATION REQUIRED${NC}"
echo "============================================================"
echo ""
echo "1. Review analysis report:"
echo "   cat docs/document_analysis.md"
echo ""
echo "2. Customize schemas if needed:"
echo "   nano shipping_doc_analyst/core/schemas.py"
echo ""
echo "3. Start annotation (interactive):"
echo "   python scripts/annotate_documents.py"
echo ""
echo "   This will guide you through annotating each PDF."
echo "   Estimated time: 3-5 minutes per document"
echo ""
echo "4. After annotation, validate:"
echo "   python scripts/validate_annotations.py"
echo ""
echo "5. Split data:"
echo "   python scripts/split_data.py"
echo ""
echo "6. Generate quality report:"
echo "   python scripts/data_quality_report.py"
echo ""
echo "7. Commit to git:"
echo "   git add ."
echo "   git commit -m 'Layer 0 complete: Ground truth annotations created'"
echo ""
echo "============================================================"
echo -e "${GREEN}✓ Layer 0 preparation scripts ready${NC}"
echo "============================================================"
echo ""
