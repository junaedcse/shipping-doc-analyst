#!/usr/bin/env python3
"""Split annotated data into train/validation/test sets with stratification."""

import json
import shutil
from pathlib import Path
from typing import Dict, List
import random

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import click

console = Console()

def get_document_type(json_path: Path) -> str:
    """Extract document type from annotation."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("document_type", "unknown")
    except:
        return "unknown"

def copy_corresponding_pdf(json_path: Path, src_base: Path, dst_base: Path):
    """Copy the PDF file corresponding to this annotation if it exists."""
    # Find the PDF with same stem in src directory
    pdf_name = json_path.stem + ".pdf"
    
    # Reconstruct PDF path in source
    relative_path = json_path.parent.name  # e.g., "invoices"
    src_pdf = src_base / relative_path / pdf_name
    
    if src_pdf.exists():
        dst_pdf = dst_base / relative_path / pdf_name
        dst_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_pdf, dst_pdf)

@click.command()
@click.option("--input-dir", type=click.Path(exists=True), default="data/ground_truth/train", 
              help="Input directory with all annotations")
@click.option("--output-base", type=click.Path(), default="data/ground_truth", 
              help="Base output directory (will create train/val/test subdirs)")
@click.option("--train-ratio", type=float, default=0.7, help="Training set ratio")
@click.option("--val-ratio", type=float, default=0.15, help="Validation set ratio")
@click.option("--test-ratio", type=float, default=0.15, help="Test set ratio")
@click.option("--seed", type=int, default=42, help="Random seed for reproducibility")
@click.option("--copy-pdfs", is_flag=True, help="Also copy corresponding PDF files")
@click.option("--pdf-dir", type=click.Path(), default="data/raw", 
              help="Directory containing original PDFs (if --copy-pdfs)")
def main(input_dir: str, output_base: str, train_ratio: float, val_ratio: float, 
         test_ratio: float, seed: int, copy_pdfs: bool, pdf_dir: str):
    """Split annotations into train/validation/test sets with stratification by document type."""
    
    random.seed(seed)
    
    input_path = Path(input_dir)
    base_dir = Path(output_base)
    pdf_base = Path(pdf_dir) if copy_pdfs else None
    
    console.print(Panel("[bold]📊 Splitting Data[/bold]", expand=False))
    console.print()
    
    # Validate ratios
    total_ratio = train_ratio + val_ratio + test_ratio
    if abs(total_ratio - 1.0) > 0.01:
        console.print(f"[red]Error: Ratios must sum to 1.0 (current: {total_ratio})[/red]")
        sys.exit(1)
    
    # Find all annotations
    json_files = list(input_path.rglob("*.json"))
    
    if not json_files:
        console.print(f"[red]⚠ No annotation files found in {input_path}[/red]")
        return
    
    console.print(f"📄 Found {len(json_files)} annotations")
    
    # Group by document type for stratification
    by_type = {}
    for json_file in json_files:
        doc_type = get_document_type(json_file)
        if doc_type not in by_type:
            by_type[doc_type] = []
        by_type[doc_type].append(json_file)
    
    # Show distribution
    console.print("\n[bold]Document Type Distribution:[/bold]")
    dist_table = Table()
    dist_table.add_column("Type", style="cyan")
    dist_table.add_column("Count", style="magenta")
    dist_table.add_column("Percentage", style="green")
    
    for doc_type, files in sorted(by_type.items()):
        pct = 100 * len(files) / len(json_files)
        dist_table.add_row(doc_type, str(len(files)), f"{pct:.1f}%")
    
    console.print(dist_table)
    
    # Warn if too few samples per type
    min_samples = min(len(files) for files in by_type.values())
    if min_samples < 3:
        console.print(f"\n[yellow]⚠ Warning: Smallest type has only {min_samples} samples.[/yellow]")
        console.print("[yellow]  Stratified split may not work well.[/yellow]")
    
    # Split each type independently (stratification)
    train_files = []
    val_files = []
    test_files = []
    
    console.print("\n[cyan]Splitting each document type...[/cyan]")
    
    for doc_type, files in by_type.items():
        # Shuffle within type
        random.shuffle(files)
        
        n_total = len(files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        # test gets the remainder to ensure all files are used
        
        type_train = files[:n_train]
        type_val = files[n_train:n_train+n_val]
        type_test = files[n_train+n_val:]
        
        train_files.extend(type_train)
        val_files.extend(type_val)
        test_files.extend(type_test)
        
        console.print(f"  {doc_type}: {len(type_train)} train, {len(type_val)} val, {len(type_test)} test")
    
    # Summary
    console.print("\n[bold]Split Summary:[/bold]")
    split_table = Table()
    split_table.add_column("Split", style="cyan")
    split_table.add_column("Count", style="magenta")
    split_table.add_column("Percentage", style="green")
    
    total = len(json_files)
    split_table.add_row("Train", str(len(train_files)), f"{100*len(train_files)/total:.1f}%")
    split_table.add_row("Validation", str(len(val_files)), f"{100*len(val_files)/total:.1f}%")
    split_table.add_row("Test", str(len(test_files)), f"{100*len(test_files)/total:.1f}%")
    split_table.add_row("TOTAL", str(total), "100.0%", style="bold")
    
    console.print(split_table)
    console.print()
    
    # Confirm before proceeding
    if not click.confirm("Proceed with split?", default=True):
        console.print("[yellow]Split cancelled[/yellow]")
        return
    
    # Create target directories
    train_dir = base_dir / "train"
    val_dir = base_dir / "validation"
    test_dir = base_dir / "test"
    
    # Clear existing directories if they exist
    for dir_path in [train_dir, val_dir, test_dir]:
        if dir_path.exists() and dir_path != input_path:
            console.print(f"[yellow]Clearing existing directory: {dir_path}[/yellow]")
            shutil.rmtree(dir_path)
    
    # Copy files to splits
    console.print("\n[cyan]Copying files...[/cyan]")
    
    with console.status("[cyan]Copying to train split...", spinner="dots"):
        for json_file in train_files:
            relative_path = json_file.relative_to(input_path)
            target = train_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(json_file, target)
            
            if copy_pdfs and pdf_base:
                copy_corresponding_pdf(json_file, pdf_base, train_dir.parent.parent / "raw_splits" / "train")
    
    with console.status("[cyan]Copying to validation split...", spinner="dots"):
        for json_file in val_files:
            relative_path = json_file.relative_to(input_path)
            target = val_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(json_file, target)
            
            if copy_pdfs and pdf_base:
                copy_corresponding_pdf(json_file, pdf_base, val_dir.parent.parent / "raw_splits" / "validation")
    
    with console.status("[cyan]Copying to test split...", spinner="dots"):
        for json_file in test_files:
            relative_path = json_file.relative_to(input_path)
            target = test_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(json_file, target)
            
            if copy_pdfs and pdf_base:
                copy_corresponding_pdf(json_file, pdf_base, test_dir.parent.parent / "raw_splits" / "test")
    
    # Save split manifest
    manifest = {
        "split_date": str(Path().resolve()),
        "seed": seed,
        "ratios": {
            "train": train_ratio,
            "validation": val_ratio,
            "test": test_ratio
        },
        "counts": {
            "total": len(json_files),
            "train": len(train_files),
            "validation": len(val_files),
            "test": len(test_files)
        },
        "document_ids": {
            "train": [f.stem for f in train_files],
            "validation": [f.stem for f in val_files],
            "test": [f.stem for f in test_files]
        }
    }
    
    manifest_path = base_dir / "split_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✓ Split manifest saved: {manifest_path}[/green]")
    
    # Final summary
    console.print("\n" + "="*60)
    console.print(Panel("[bold green]✓ Data split complete![/bold green]", style="green", expand=False))
    console.print()
    console.print("[bold]Output directories:[/bold]")
    console.print(f"  📁 Train:      {train_dir}")
    console.print(f"  📁 Validation: {val_dir}")
    console.print(f"  📁 Test:       {test_dir}")
    console.print()
    console.print("[cyan]Next steps:[/cyan]")
    console.print("1. Generate quality report: python scripts/data_quality_report.py")
    console.print("2. Commit to git: git add . && git commit -m 'Layer 0 complete'")
    console.print("3. Proceed to Layer 1 (Data Ingestion)")

if __name__ == "__main__":
    main()
