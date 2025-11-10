#!/usr/bin/env python3
"""Analyze PDF documents to understand structure and common patterns."""

import sys
from pathlib import Path
from collections import Counter, defaultdict
import PyPDF2
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import click

console = Console()

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        console.print(f"[red]Error reading {pdf_path.name}: {e}[/red]")
        return ""

def detect_common_keywords(text: str, doc_type: str) -> dict:
    """Detect presence of common keywords for document type."""
    keywords = {
        "invoice": ["invoice", "bill", "amount", "total", "tax", "due", "payment"],
        "purchase_order": ["purchase order", "po", "order", "supplier", "delivery"],
        "shipping_order": ["shipping", "shipment", "consignee", "shipper", "cargo", "vessel", "container"]
    }
    
    text_lower = text.lower()
    found = {}
    
    for keyword in keywords.get(doc_type, []):
        count = text_lower.count(keyword)
        if count > 0:
            found[keyword] = count
    
    return found

def analyze_document(pdf_path: Path, doc_type: str) -> dict:
    """Analyze a single PDF document."""
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        return None
    
    # Basic statistics
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    words = text.split()
    
    # Detect keywords
    keywords = detect_common_keywords(text, doc_type)
    
    # Check for dates (simple pattern)
    date_count = text.count('/') + text.count('-')
    
    # Check for numbers (potential amounts)
    number_count = sum(1 for word in words if any(c.isdigit() for c in word))
    
    return {
        "filename": pdf_path.name,
        "pages": len(text.split('\f')) if '\f' in text else 1,
        "lines": len(lines),
        "words": len(words),
        "keywords": keywords,
        "potential_dates": date_count,
        "potential_numbers": number_count,
        "text_preview": text[:500]
    }

@click.command()
@click.option("--data-dir", type=click.Path(exists=True), default="data/raw", help="Directory containing PDFs")
@click.option("--output", type=click.Path(), default="docs/document_analysis.md", help="Output analysis file")
def main(data_dir: str, output: str):
    """Analyze PDF documents and generate structure report."""
    
    data_path = Path(data_dir)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel("[bold blue]Document Structure Analysis[/bold blue]", expand=False))
    
    # Analyze each document type
    doc_types = {
        "invoice": "invoices",
        "purchase_order": "purchase_orders",
        "shipping_order": "shipping_orders"
    }
    
    all_results = {}
    
    for doc_type, folder_name in doc_types.items():
        folder_path = data_path / folder_name
        
        if not folder_path.exists():
            console.print(f"[yellow]Folder not found: {folder_path}[/yellow]")
            continue
        
        pdfs = list(folder_path.glob("*.pdf"))
        
        if not pdfs:
            console.print(f"[yellow]No PDFs in {folder_name}[/yellow]")
            continue
        
        console.print(f"\n[cyan]Analyzing {len(pdfs)} {doc_type}(s)...[/cyan]")
        
        results = []
        for pdf_path in pdfs[:5]:  # Analyze first 5 of each type
            result = analyze_document(pdf_path, doc_type)
            if result:
                results.append(result)
        
        all_results[doc_type] = results
        
        # Display summary table
        if results:
            table = Table(title=f"{doc_type.upper()} Analysis")
            table.add_column("Filename", style="cyan")
            table.add_column("Pages", style="magenta")
            table.add_column("Lines", style="green")
            table.add_column("Keywords", style="yellow")
            
            for r in results:
                table.add_row(
                    r["filename"][:30],
                    str(r["pages"]),
                    str(r["lines"]),
                    str(len(r["keywords"]))
                )
            
            console.print(table)
    
    # Generate markdown report
    console.print(f"\n[cyan]Generating analysis report...[/cyan]")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Document Analysis Report\n\n")
        f.write("Generated from PDF structure analysis.\n\n")
        
        for doc_type, results in all_results.items():
            if not results:
                continue
            
            f.write(f"## {doc_type.upper().replace('_', ' ')}\n\n")
            f.write(f"Sample files examined: {len(results)}\n\n")
            
            # Common keywords
            all_keywords = Counter()
            for r in results:
                all_keywords.update(r["keywords"])
            
            f.write("### Common Keywords Found\n\n")
            for keyword, count in all_keywords.most_common(10):
                f.write(f"- {keyword}: {count} occurrences\n")
            
            f.write("\n### Common Fields to Extract\n\n")
            
            # Suggest fields based on document type
            if doc_type == "invoice":
                fields = [
                    "Invoice number",
                    "Invoice date",
                    "Seller/vendor name",
                    "Seller address",
                    "Buyer name",
                    "Buyer address",
                    "Line items (description, quantity, price)",
                    "Subtotal",
                    "Tax",
                    "Total amount",
                    "Currency",
                    "Payment terms",
                    "Due date"
                ]
            elif doc_type == "purchase_order":
                fields = [
                    "PO number",
                    "PO date",
                    "Buyer name",
                    "Buyer address",
                    "Supplier name",
                    "Supplier address",
                    "Line items",
                    "Total amount",
                    "Delivery date",
                    "Shipping address",
                    "Payment terms"
                ]
            else:  # shipping_order
                fields = [
                    "Order/BOL number",
                    "Ship date",
                    "Shipper name",
                    "Shipper address",
                    "Consignee name",
                    "Consignee address",
                    "Cargo items",
                    "Total weight",
                    "Origin",
                    "Destination",
                    "Carrier",
                    "Tracking number"
                ]
            
            for field in fields:
                f.write(f"- [ ] {field}\n")
            
            f.write("\n### Document Statistics\n\n")
            
            avg_pages = sum(r["pages"] for r in results) / len(results)
            avg_lines = sum(r["lines"] for r in results) / len(results)
            
            f.write(f"- Average pages: {avg_pages:.1f}\n")
            f.write(f"- Average lines: {avg_lines:.0f}\n")
            
            f.write("\n### Challenges/Notes\n\n")
            f.write("- Add your observations here\n")
            f.write("- Note any quality issues\n")
            f.write("- Note variations in format\n")
            
            f.write("\n---\n\n")
    
    console.print(f"[green]✓ Analysis report saved to: {output_path}[/green]")
    console.print(f"\n[yellow]Next steps:[/yellow]")
    console.print(f"1. Review the report: {output_path}")
    console.print(f"2. Customize schemas if needed: shipping_doc_analyst/core/schemas.py")
    console.print(f"3. Start annotation: python scripts/annotate_documents.py")

if __name__ == "__main__":
    main()
