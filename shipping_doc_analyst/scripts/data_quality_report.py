#!/usr/bin/env python3
"""Generate comprehensive data quality report for annotated datasets."""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import click

console = Console()

def analyze_split(split_dir: Path) -> dict:
    """Analyze a single split (train/val/test)."""
    json_files = list(split_dir.rglob("*.json"))
    
    if not json_files:
        return None
    
    # Collect statistics
    doc_types = Counter()
    field_counts = defaultdict(list)
    total_items = 0
    has_company_info = 0
    has_amounts = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            doc_type = data.get("document_type", "unknown")
            doc_types[doc_type] += 1
            
            entities = data.get("entities", {})
            field_counts[doc_type].append(len(entities))
            
            # Count line items / cargo items
            if "line_items" in entities:
                total_items += len(entities.get("line_items", []))
            elif "cargo_items" in entities:
                total_items += len(entities.get("cargo_items", []))
            
            # Check for company information
            if any(k in entities for k in ["seller", "buyer", "shipper", "consignee", "supplier"]):
                has_company_info += 1
            
            # Check for financial amounts
            if any(k in entities for k in ["total", "subtotal", "tax", "total_weight"]):
                has_amounts += 1
                
        except Exception as e:
            console.print(f"[yellow]Warning: Error reading {json_file.name}: {e}[/yellow]")
    
    return {
        "total_docs": len(json_files),
        "doc_types": dict(doc_types),
        "field_counts": {k: sum(v)/len(v) if v else 0 for k, v in field_counts.items()},
        "total_items": total_items,
        "has_company_info": has_company_info,
        "has_amounts": has_amounts
    }

@click.command()
@click.option("--data-dir", type=click.Path(exists=True), default="data/ground_truth", 
              help="Ground truth directory containing splits")
@click.option("--output", type=click.Path(), default="docs/data_quality_report.md",
              help="Output markdown report path")
def main(data_dir: str, output: str):
    """Generate comprehensive data quality report for all splits."""
    
    data_path = Path(data_dir)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel("[bold]📊 Generating Data Quality Report[/bold]", expand=False))
    console.print()
    
    # Analyze each split
    splits = ["train", "validation", "test"]
    split_data = {}
    
    for split in splits:
        split_dir = data_path / split
        
        if not split_dir.exists():
            console.print(f"[yellow]⚠ {split} directory not found, skipping[/yellow]")
            continue
        
        console.print(f"[cyan]Analyzing {split} set...[/cyan]")
        stats = analyze_split(split_dir)
        
        if stats:
            split_data[split] = stats
            console.print(f"  ✓ {stats['total_docs']} documents analyzed")
    
    if not split_data:
        console.print("[red]No data found to analyze![/red]")
        return
    
    console.print()
    
    # Display summary tables
    for split, stats in split_data.items():
        table = Table(title=f"{split.upper()} Set Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Documents", str(stats['total_docs']))
        table.add_row("Total Items", str(stats['total_items']))
        table.add_row("Avg Items/Doc", f"{stats['total_items']/stats['total_docs']:.1f}")
        table.add_row("Has Company Info", f"{100*stats['has_company_info']/stats['total_docs']:.1f}%")
        table.add_row("Has Amounts", f"{100*stats['has_amounts']/stats['total_docs']:.1f}%")
        
        console.print(table)
        console.print()
        
        # Document type breakdown
        if stats['doc_types']:
            type_table = Table(title=f"{split.upper()} - Document Types")
            type_table.add_column("Type", style="cyan")
            type_table.add_column("Count", style="magenta")
            type_table.add_column("Percentage", style="green")
            type_table.add_column("Avg Fields", style="yellow")
            
            for doc_type, count in stats['doc_types'].items():
                pct = 100 * count / stats['total_docs']
                avg_fields = stats['field_counts'].get(doc_type, 0)
                
                type_table.add_row(
                    doc_type,
                    str(count),
                    f"{pct:.1f}%",
                    f"{avg_fields:.1f}"
                )
            
            console.print(type_table)
            console.print()
    
    # Generate markdown report
    console.print("[cyan]Generating markdown report...[/cyan]")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overall Summary\n\n")
        
        total_docs = sum(s['total_docs'] for s in split_data.values())
        f.write(f"- **Total Documents**: {total_docs}\n")
        
        for split, stats in split_data.items():
            f.write(f"- **{split.capitalize()}**: {stats['total_docs']} documents ({100*stats['total_docs']/total_docs:.1f}%)\n")
        
        f.write("\n")
        
        # Per-split details
        for split, stats in split_data.items():
            f.write(f"## {split.upper()} Set\n\n")
            
            f.write("### Statistics\n\n")
            f.write(f"- Total Documents: {stats['total_docs']}\n")
            f.write(f"- Total Items (line items/cargo): {stats['total_items']}\n")
            f.write(f"- Average Items per Document: {stats['total_items']/stats['total_docs']:.1f}\n")
            f.write(f"- Documents with Company Info: {stats['has_company_info']} ({100*stats['has_company_info']/stats['total_docs']:.1f}%)\n")
            f.write(f"- Documents with Amounts: {stats['has_amounts']} ({100*stats['has_amounts']/stats['total_docs']:.1f}%)\n")
            f.write("\n")
            
            f.write("### Document Type Distribution\n\n")
            f.write("| Type | Count | Percentage | Avg Fields |\n")
            f.write("|------|-------|------------|------------|\n")
            
            for doc_type, count in stats['doc_types'].items():
                pct = 100 * count / stats['total_docs']
                avg_fields = stats['field_counts'].get(doc_type, 0)
                f.write(f"| {doc_type} | {count} | {pct:.1f}% | {avg_fields:.1f} |\n")
            
            f.write("\n")
        
        # Quality checks
        f.write("## Quality Checks\n\n")
        
        all_good = True
        
        # Check 1: Balanced splits
        if len(split_data) >= 2:
            doc_counts = [s['total_docs'] for s in split_data.values()]
            max_count = max(doc_counts)
            min_count = min(doc_counts)
            
            if max_count > 0 and min_count / max_count < 0.5:
                f.write("- ⚠️ **Warning**: Splits are imbalanced (difference > 50%)\n")
                all_good = False
            else:
                f.write("- ✓ Split sizes are balanced\n")
        
        # Check 2: Document type distribution
        for split, stats in split_data.items():
            if len(stats['doc_types']) < 2:
                f.write(f"- ⚠️ **Warning**: {split} has only {len(stats['doc_types'])} document type(s)\n")
                all_good = False
        
        if all_good:
            f.write("- ✓ Document types are well distributed\n")
        
        f.write("\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        
        total_all = sum(s['total_docs'] for s in split_data.values())
        
        if total_all < 30:
            f.write("- ⚠️ Dataset is small (<30 documents). Consider annotating more for better model performance.\n")
        elif total_all < 100:
            f.write("- ℹ️ Dataset is moderate (30-100 documents). Good for initial testing.\n")
        else:
            f.write("- ✓ Dataset size is good (100+ documents).\n")
        
        f.write("\n")
        
        # Check annotation completeness
        avg_company = sum(s['has_company_info'] for s in split_data.values()) / sum(s['total_docs'] for s in split_data.values())
        
        if avg_company < 0.5:
            f.write("- ⚠️ Less than 50% of documents have company information. Consider adding more details.\n")
        else:
            f.write("- ✓ Good coverage of company information in annotations.\n")
        
        f.write("\n---\n\n")
        f.write("**Status**: ")
        
        if all_good and total_all >= 30:
            f.write("✅ READY FOR TRAINING\n")
        elif total_all < 30:
            f.write("⚠️ MORE DATA RECOMMENDED\n")
        else:
            f.write("⚠️ REVIEW WARNINGS\n")
    
    console.print(f"[green]✓ Report saved: {output_path}[/green]")
    console.print()
    
    # Final status
    total_all = sum(s['total_docs'] for s in split_data.values())
    
    if total_all >= 30:
        console.print(Panel("[bold green]✅ Dataset Quality: GOOD[/bold green]\n"
                           f"Total documents: {total_all}\n"
                           "Ready to proceed to next layer", 
                           style="green", expand=False))
    else:
        console.print(Panel(f"[bold yellow]⚠️ Dataset Quality: NEEDS MORE DATA[/bold yellow]\n"
                           f"Total documents: {total_all}\n"
                           "Recommend at least 30 documents total", 
                           style="yellow", expand=False))
    
    console.print("\n[cyan]Review full report:[/cyan]")
    console.print(f"  {output_path}")

if __name__ == "__main__":
    main()
