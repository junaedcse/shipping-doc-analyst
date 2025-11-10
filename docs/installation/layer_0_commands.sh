# ============================================================
# LAYER 0: QUICK REFERENCE COMMANDS
# ============================================================
# Copy-paste these commands to execute Layer 0 step by step
# ============================================================

# PREREQUISITE: Ensure Layer -1 is complete and venv is activated
source .venv/bin/activate

# ============================================================
# STEP 1: Copy Your PDFs to Project
# ============================================================

# Replace /path/to/your/pdfs with your actual paths
cp /path/to/your/invoices/*.pdf data/raw/invoices/
cp /path/to/your/purchase_orders/*.pdf data/raw/purchase_orders/
cp /path/to/your/shipping_orders/*.pdf data/raw/shipping_orders/

# Verify PDFs copied
ls -lh data/raw/invoices/
ls -lh data/raw/purchase_orders/
ls -lh data/raw/shipping_orders/

# Count total PDFs
find data/raw -name "*.pdf" | wc -l

# ============================================================
# STEP 2: Analyze Document Structure
# ============================================================

# Analyze PDFs to understand their structure
python scripts/analyze_documents.py

# Review the analysis
cat docs/document_analysis.md

# ============================================================
# STEP 3: (Optional) Customize Entity Schemas
# ============================================================

# If your documents have different fields than expected,
# edit the schemas to match your documents
nano shipping_doc_analyst/core/schemas.py

# Or use your preferred editor
# code shipping_doc_analyst/core/schemas.py

# ============================================================
# STEP 4: Annotate Documents (MAIN WORK)
# ============================================================

# Start interactive annotation
python scripts/annotate_documents.py

# This will:
# - Show each PDF filename
# - Prompt you to fill in entity values
# - Save JSON annotations as you go
# - Allow you to pause and resume

# Resume annotation if you paused
python scripts/annotate_documents.py --resume

# Estimate: 3-5 minutes per document
# For 60 documents: ~3-5 hours total (spread over multiple sessions)

# ============================================================
# STEP 5: Validate Annotations
# ============================================================

# Check all annotations for completeness
python scripts/validate_annotations.py

# Show detailed issues if any
python scripts/validate_annotations.py --detailed

# Fix any issues by editing the JSON files directly
# nano data/ground_truth/train/invoices/[filename].json

# Re-run validation until all pass
python scripts/validate_annotations.py

# ============================================================
# STEP 6: Split Data into Train/Val/Test
# ============================================================

# Split with default ratios (70/15/15)
python scripts/split_data.py

# Or specify custom ratios
python scripts/split_data.py --train-ratio 0.7 --val-ratio 0.15 --test-ratio 0.15

# Verify splits created
ls -lh data/ground_truth/train/
ls -lh data/ground_truth/validation/
ls -lh data/ground_truth/test/

# Count files in each split
find data/ground_truth/train -name "*.json" | wc -l
find data/ground_truth/validation -name "*.json" | wc -l
find data/ground_truth/test -name "*.json" | wc -l

# ============================================================
# STEP 7: Generate Quality Report
# ============================================================

# Generate comprehensive quality report
python scripts/data_quality_report.py

# Review the report
cat docs/data_quality_report.md

# ============================================================
# STEP 8: Commit to Git
# ============================================================

# Add all changes
git add .

# Create commit
git commit -m "Layer 0 complete: Ground truth annotations created

- Analyzed document structure
- Created entity schemas
- Annotated all PDFs with ground truth
- Validated all annotations
- Split data into train/validation/test (70/15/15)
- Generated quality report
"

# View git status
git status

# ============================================================
# VERIFICATION CHECKLIST
# ============================================================

# Run these checks to verify Layer 0 is complete:

# 1. All PDFs have annotations
python -c "
from pathlib import Path
pdfs = len(list(Path('data/raw').rglob('*.pdf')))
jsons = len(list(Path('data/ground_truth/train').rglob('*.json')))
print(f'PDFs: {pdfs}, Annotations: {jsons}')
print('✓ Complete' if pdfs == jsons else '✗ Missing annotations')
"

# 2. All annotations are valid
python scripts/validate_annotations.py

# 3. Data is split
test -d data/ground_truth/train && \
test -d data/ground_truth/validation && \
test -d data/ground_truth/test && \
echo "✓ Splits created" || echo "✗ Splits missing"

# 4. Quality report exists
test -f docs/data_quality_report.md && \
echo "✓ Quality report exists" || echo "✗ Report missing"

# ============================================================
# LAYER 0 COMPLETION
# ============================================================

# If all checks pass, Layer 0 is complete!
# Proceed to Layer 1: Data Ingestion

echo ""
echo "============================================================"
echo "✓ LAYER 0 COMPLETE"
echo "============================================================"
echo ""
echo "You now have:"
echo "  - Analyzed document structure"
echo "  - Ground truth annotations for all PDFs"
echo "  - Validated data quality"
echo "  - Train/validation/test splits"
echo ""
echo "Next: Proceed to Layer 1 (Data Ingestion)"
echo ""
