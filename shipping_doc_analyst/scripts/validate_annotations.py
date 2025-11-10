#!/usr/bin/env python3
"""Validate ground truth annotations for completeness and correctness."""

import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import click

console = Console()

def validate_annotation(annotation_path: Path) -> Tuple[bool, List[str]]:
    """Validate a single annotation file. Returns (is_valid, issues_list)."""
    issues = []
    
    # Check if file is valid JSON
    try:
        with open(annotation_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    # Check required top-level fields
    required_top_level = ["document_id", "filename", "document_type", "entities"]
    for field in required_top_level:
        if field not in data:
            issues.append(f"Missing required field: '{field}'")
    
    # Validate document_type
    if "document_type" in data:
        valid_types = ["invoice", "purchase_order", "shipping_order"]
        if data["document_type"] not in valid_types:
            issues.append(f"Invalid document_type: '{data['document_type']}' (must be one of {valid_types})")
    
    # Validate entities structure
    if "entities" in data:
        entities = data["entities"]
        
        if not isinstance(entities, dict):
            issues.append("'entities' must be a dictionary")
        else:
            # Check for document_type in entities (should match top level)
            if "document_type" in entities and "document_type" in data:
                if entities["document_type"] != data["document_type"]:
                    issues.append(f"Mismatched document_type: top='{data['document_type']}' vs entities='{entities['document_type']}'")
            
            # Type-specific validation
            doc_type = data.get("document_type")
            
            if doc_type == "invoice":
                if "invoice_number" not in entities:
                    issues.append("Invoice missing 'invoice_number'")
            
            elif doc_type == "purchase_order":
                if "po_number" not in entities:
                    issues.append("Purchase order missing 'po_number'")
            
            elif doc_type == "shipping_order":
                if "order_number" not in entities:
                    issues.append("Shipping order missing 'order_number'")
            
            # Check if entities is empty
            if len(entities) <= 1:  # Only document_type field
                issues.append("'entities' has no actual data (only document_type)")
    
    # Validate metadata if present
    if "annotation_metadata" in data:
        metadata = data["annotation_metadata"]
        if not isinstance(metadata, dict):
            issues.append("'annotation_metadata' must be a dictionary")
    
    return len(issues) == 0, issues

def get_annotation_stats(annotation_path: Path) -> Dict:
    """Extract statistics from annotation."""
    try:
        with open(annotation_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entities = data.get("entities", {})
        
        # Count fields
        field_count = len(entities)
        
        # Count line items / cargo items
        items_count = 0
        if "line_items" in entities:
            items_count = len(entities.get("line_items", []))
        elif "cargo_items" in entities:
            items_count = len(entities.get("cargo_items", []))
        
        return {
            "document_type": data.get("document_type", "unknown"),
            "field_count": field_count,
            "items_count": items_count,
            "has_seller_buyer": ("seller" in entities or "buyer" in entities or 
                                  "shipper" in entities or "consignee" in entities),
            "has_amounts": ("total" in entities or "subtotal" in entities or 
                           "total_weight" in entities)
        }
    except:
        return {}

@click.command()
@click.option("--annotation-dir", type=click.Path(exists=True), default="data/ground_truth/train", 
              help="Directory containing annotations")
@click.option("--detailed", is_flag=True, help="Show detailed issue breakdown")
def main(annotation_dir: str, detailed: bool):
    """Validate all annotation files for quality and completeness."""
    
    annotation_path = Path(annotation_dir)
    
    console.print(Panel("[bold]🔍 Validating Annotations[/bold]", expand=False))
    console.print()
    
    # Find all JSON files
    json_files = list(annotation_path.rglob("*.json"))
    
    if not json_files:
        console.print("[yellow]⚠ No annotation files found![/yellow]")
        console.print(f"Looking in: {annotation_path}")
        return
    
    console.print(f"📊 Found {len(json_files)} annotation files\n")
    
    # Validate each file
    results = []
    stats_by_type = {}
    
    with console.status("[cyan]Validating annotations...", spinner="dots"):
        for json_file in json_files:
            is_valid, issues = validate_annotation(json_file)
            stats = get_annotation_stats(json_file)
            
            results.append({
                "file": json_file.name,
                "path": str(json_file.relative_to(annotation_path)),
                "valid": is_valid,
                "issues": issues,
                "stats": stats
            })
            
            # Collect stats by type
            doc_type = stats.get("document_type", "unknown")
            if doc_type not in stats_by_type:
                stats_by_type[doc_type] = []
            stats_by_type[doc_type].append(stats)
    
    # Create validation table
    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = len(results) - valid_count
    
    # Summary table
    summary_table = Table(title="Validation Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="bold")
    
    summary_table.add_row("Total Files", str(len(results)))
    summary_table.add_row("Valid", f"[green]{valid_count}[/green]")
    summary_table.add_row("Invalid", f"[red]{invalid_count}[/red]" if invalid_count > 0 else "0")
    summary_table.add_row("Success Rate", f"{100*valid_count/len(results):.1f}%")
    
    console.print(summary_table)
    console.print()
    
    # Statistics by document type
    if stats_by_type:
        type_table = Table(title="Statistics by Document Type")
        type_table.add_column("Type", style="cyan")
        type_table.add_column("Count", style="magenta")
        type_table.add_column("Avg Fields", style="green")
        type_table.add_column("Avg Items", style="yellow")
        
        for doc_type, stats_list in stats_by_type.items():
            count = len(stats_list)
            avg_fields = sum(s.get("field_count", 0) for s in stats_list) / count
            avg_items = sum(s.get("items_count", 0) for s in stats_list) / count
            
            type_table.add_row(
                doc_type,
                str(count),
                f"{avg_fields:.1f}",
                f"{avg_items:.1f}"
            )
        
        console.print(type_table)
        console.print()
    
    # Show invalid files
    if invalid_count > 0:
        console.print("[bold red]⚠ Files with Issues:[/bold red]\n")
        
        for result in results:
            if not result["valid"]:
                console.print(f"[red]✗[/red] {result['path']}")
                if detailed:
                    for issue in result["issues"]:
                        console.print(f"  • {issue}")
                    console.print()
        
        console.print()
    
    # Final verdict
    if valid_count == len(results):
        console.print(Panel("[bold green]✓ All annotations are valid![/bold green]", 
                           style="green", expand=False))
        console.print("\n[cyan]Next step: Split data into train/val/test[/cyan]")
        console.print("  python scripts/split_data.py\n")
        sys.exit(0)
    else:
        console.print(Panel(f"[bold red]✗ {invalid_count} annotation(s) have issues[/bold red]\n"
                           "[yellow]Please fix them before proceeding[/yellow]", 
                           style="red", expand=False))
        console.print("\n[cyan]To see detailed issues:[/cyan]")
        console.print("  python scripts/validate_annotations.py --detailed\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
