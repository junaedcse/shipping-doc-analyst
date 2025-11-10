#!/usr/bin/env python3
"""Interactive tool for annotating PDF documents with ground truth entities."""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

def list_unannotated_pdfs(data_dir: Path, ground_truth_dir: Path) -> List[Path]:
    """Find PDFs that don't have annotations yet."""
    all_pdfs = list(data_dir.rglob("*.pdf"))
    
    unannotated = []
    for pdf_path in all_pdfs:
        # Check if annotation exists
        relative_path = pdf_path.relative_to(data_dir)
        annotation_path = ground_truth_dir / relative_path.parent / f"{pdf_path.stem}.json"
        
        if not annotation_path.exists():
            unannotated.append(pdf_path)
    
    return unannotated

def get_optional_field(prompt_text: str, default: str = "") -> str:
    """Get optional field with default empty string."""
    value = Prompt.ask(prompt_text, default=default)
    return value if value else None

def annotate_invoice(pdf_path: Path) -> Dict:
    """Collect invoice annotations interactively."""
    console.print(Panel(f"[bold blue]Annotating Invoice: {pdf_path.name}[/bold blue]"))
    console.print("[yellow]💡 Tip: Open the PDF in another window for reference[/yellow]\n")
    
    entities = {"document_type": "invoice"}
    
    # Required fields
    entities["invoice_number"] = Prompt.ask("📄 Invoice Number")
    
    # Optional fields
    entities["invoice_date"] = get_optional_field("📅 Invoice Date (YYYY-MM-DD)")
    entities["currency"] = Prompt.ask("💱 Currency", default="USD")
    
    # Seller information
    if Confirm.ask("\n➕ Add seller information?", default=True):
        console.print("[cyan]Seller/Vendor:[/cyan]")
        seller = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            seller["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        seller["phone"] = get_optional_field("  Phone")
        seller["email"] = get_optional_field("  Email")
        entities["seller"] = seller
    
    # Buyer information
    if Confirm.ask("\n➕ Add buyer information?", default=True):
        console.print("[cyan]Buyer:[/cyan]")
        buyer = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            buyer["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        buyer["phone"] = get_optional_field("  Phone")
        buyer["email"] = get_optional_field("  Email")
        entities["buyer"] = buyer
    
    # Line items
    line_items = []
    if Confirm.ask("\n➕ Add line items?", default=True):
        console.print("[cyan]Line Items:[/cyan]")
        
        while True:
            item = {}
            item["description"] = Prompt.ask(f"  📦 Item {len(line_items)+1} Description")
            
            qty = get_optional_field("  Quantity")
            if qty:
                try:
                    item["quantity"] = float(qty)
                except ValueError:
                    pass
            
            item["unit"] = get_optional_field("  Unit (pcs/kg/etc)")
            
            price = get_optional_field("  Unit Price")
            if price:
                try:
                    item["unit_price"] = float(price)
                except ValueError:
                    pass
            
            total = get_optional_field("  Total Price")
            if total:
                try:
                    item["total_price"] = float(total)
                except ValueError:
                    pass
            
            line_items.append(item)
            
            if not Confirm.ask("  ➕ Add another item?", default=False):
                break
    
    entities["line_items"] = line_items
    
    # Totals
    console.print("\n[cyan]Financial Totals:[/cyan]")
    
    subtotal = get_optional_field("💰 Subtotal")
    if subtotal:
        try:
            entities["subtotal"] = float(subtotal)
        except ValueError:
            pass
    
    tax = get_optional_field("💰 Tax")
    if tax:
        try:
            entities["tax"] = float(tax)
        except ValueError:
            pass
    
    total = get_optional_field("💰 Total Amount (required)")
    if total:
        try:
            entities["total"] = float(total)
        except ValueError:
            entities["total"] = 0.0
    
    entities["payment_terms"] = get_optional_field("📋 Payment Terms")
    entities["due_date"] = get_optional_field("📅 Due Date (YYYY-MM-DD)")
    entities["notes"] = get_optional_field("📝 Notes")
    
    return entities

def annotate_purchase_order(pdf_path: Path) -> Dict:
    """Collect purchase order annotations interactively."""
    console.print(Panel(f"[bold green]Annotating Purchase Order: {pdf_path.name}[/bold green]"))
    console.print("[yellow]💡 Tip: Open the PDF in another window for reference[/yellow]\n")
    
    entities = {"document_type": "purchase_order"}
    
    # Required fields
    entities["po_number"] = Prompt.ask("📄 PO Number")
    
    # Optional fields
    entities["po_date"] = get_optional_field("📅 PO Date (YYYY-MM-DD)")
    entities["currency"] = Prompt.ask("💱 Currency", default="USD")
    
    # Buyer information
    if Confirm.ask("\n➕ Add buyer information?", default=True):
        console.print("[cyan]Buyer:[/cyan]")
        buyer = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            buyer["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        entities["buyer"] = buyer
    
    # Supplier information
    if Confirm.ask("\n➕ Add supplier information?", default=True):
        console.print("[cyan]Supplier:[/cyan]")
        supplier = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            supplier["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        entities["supplier"] = supplier
    
    # Line items
    line_items = []
    if Confirm.ask("\n➕ Add line items?", default=True):
        console.print("[cyan]Line Items:[/cyan]")
        
        while True:
            item = {"description": Prompt.ask(f"  📦 Item {len(line_items)+1} Description")}
            
            qty = get_optional_field("  Quantity")
            if qty:
                try:
                    item["quantity"] = float(qty)
                except ValueError:
                    pass
            
            item["unit"] = get_optional_field("  Unit")
            
            price = get_optional_field("  Unit Price")
            if price:
                try:
                    item["unit_price"] = float(price)
                except ValueError:
                    pass
            
            line_items.append(item)
            
            if not Confirm.ask("  ➕ Add another item?", default=False):
                break
    
    entities["line_items"] = line_items
    
    # Additional fields
    console.print("\n[cyan]Additional Information:[/cyan]")
    
    total = get_optional_field("💰 Total Amount")
    if total:
        try:
            entities["total"] = float(total)
        except ValueError:
            pass
    
    entities["delivery_date"] = get_optional_field("📅 Delivery Date (YYYY-MM-DD)")
    
    if Confirm.ask("Add delivery address?"):
        entities["delivery_address"] = {"full_address": Prompt.ask("  Delivery Address")}
    
    entities["payment_terms"] = get_optional_field("📋 Payment Terms")
    entities["notes"] = get_optional_field("📝 Notes")
    
    return entities

def annotate_shipping_order(pdf_path: Path) -> Dict:
    """Collect shipping order annotations interactively."""
    console.print(Panel(f"[bold magenta]Annotating Shipping Order: {pdf_path.name}[/bold magenta]"))
    console.print("[yellow]💡 Tip: Open the PDF in another window for reference[/yellow]\n")
    
    entities = {"document_type": "shipping_order"}
    
    # Required fields
    entities["order_number"] = Prompt.ask("📄 Order/BOL Number")
    
    # Optional fields
    entities["ship_date"] = get_optional_field("📅 Ship Date (YYYY-MM-DD)")
    
    # Shipper information
    if Confirm.ask("\n➕ Add shipper information?", default=True):
        console.print("[cyan]Shipper:[/cyan]")
        shipper = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            shipper["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        entities["shipper"] = shipper
    
    # Consignee information
    if Confirm.ask("\n➕ Add consignee information?", default=True):
        console.print("[cyan]Consignee:[/cyan]")
        consignee = {"name": Prompt.ask("  Company Name")}
        
        if Confirm.ask("  Add address?"):
            consignee["address"] = {"full_address": Prompt.ask("  Full Address")}
        
        entities["consignee"] = consignee
    
    # Cargo items
    cargo_items = []
    if Confirm.ask("\n➕ Add cargo items?", default=True):
        console.print("[cyan]Cargo Items:[/cyan]")
        
        while True:
            item = {"description": Prompt.ask(f"  📦 Item {len(cargo_items)+1} Description")}
            
            qty = get_optional_field("  Quantity")
            if qty:
                try:
                    item["quantity"] = float(qty)
                except ValueError:
                    pass
            
            weight = get_optional_field("  Weight")
            if weight:
                try:
                    item["weight"] = float(weight)
                except ValueError:
                    pass
            
            item["weight_unit"] = Prompt.ask("  Weight Unit", default="kg")
            item["dimensions"] = get_optional_field("  Dimensions")
            item["package_type"] = get_optional_field("  Package Type (carton/pallet/etc)")
            
            cargo_items.append(item)
            
            if not Confirm.ask("  ➕ Add another item?", default=False):
                break
    
    entities["cargo_items"] = cargo_items
    
    # Shipping details
    console.print("\n[cyan]Shipping Details:[/cyan]")
    
    total_weight = get_optional_field("⚖️  Total Weight")
    if total_weight:
        try:
            entities["total_weight"] = float(total_weight)
        except ValueError:
            pass
    
    entities["weight_unit"] = Prompt.ask("Weight Unit", default="kg")
    entities["origin"] = get_optional_field("📍 Origin Port/Location")
    entities["destination"] = get_optional_field("📍 Destination Port/Location")
    entities["carrier"] = get_optional_field("🚢 Carrier Name")
    entities["tracking_number"] = get_optional_field("🔢 Tracking Number")
    entities["vessel_name"] = get_optional_field("🚢 Vessel Name")
    entities["container_number"] = get_optional_field("📦 Container Number")
    entities["notes"] = get_optional_field("📝 Notes")
    
    return entities

@click.command()
@click.option("--data-dir", type=click.Path(exists=True), default="data/raw", help="Directory containing PDFs")
@click.option("--output-dir", type=click.Path(), default="data/ground_truth/train", help="Output directory for annotations")
@click.option("--resume", is_flag=True, help="Resume from where you left off")
def main(data_dir: str, output_dir: str, resume: bool):
    """Interactive PDF annotation tool - creates ground truth labels."""
    
    data_path = Path(data_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel("[bold green]📝 PDF Annotation Tool[/bold green]", expand=False))
    console.print()
    
    # Find unannotated PDFs
    unannotated = list_unannotated_pdfs(data_path, output_path)
    
    if not unannotated:
        console.print("[green]✓ All PDFs are annotated![/green]")
        console.print("\n[cyan]Next step: Split data[/cyan]")
        console.print("  python scripts/split_data.py")
        return
    
    console.print(f"📊 Found {len(unannotated)} unannotated PDFs\n")
    
    # Group by type
    by_type = {}
    for pdf_path in unannotated:
        if "invoice" in str(pdf_path).lower():
            doc_type = "invoice"
        elif "purchase" in str(pdf_path).lower() or "po" in str(pdf_path).lower():
            doc_type = "purchase_order"
        elif "shipping" in str(pdf_path).lower() or "bol" in str(pdf_path).lower():
            doc_type = "shipping_order"
        else:
            doc_type = "unknown"
        
        if doc_type not in by_type:
            by_type[doc_type] = []
        by_type[doc_type].append(pdf_path)
    
    # Show summary
    table = Table(title="Documents to Annotate")
    table.add_column("Type", style="cyan")
    table.add_column("Count", style="magenta")
    
    for doc_type, files in by_type.items():
        table.add_row(doc_type, str(len(files)))
    
    console.print(table)
    console.print()
    
    if not Confirm.ask("Start annotation?", default=True):
        console.print("[yellow]Annotation cancelled[/yellow]")
        return
    
    # Annotate documents
    for i, pdf_path in enumerate(unannotated):
        console.print(f"\n[bold]Progress: {i+1}/{len(unannotated)}[/bold]")
        console.print(f"📄 File: [cyan]{pdf_path}[/cyan]\n")
        
        # Determine document type
        if "invoice" in str(pdf_path).lower():
            doc_type = "invoice"
            entities = annotate_invoice(pdf_path)
        elif "purchase" in str(pdf_path).lower() or "po" in str(pdf_path).lower():
            doc_type = "purchase_order"
            entities = annotate_purchase_order(pdf_path)
        elif "shipping" in str(pdf_path).lower() or "bol" in str(pdf_path).lower():
            doc_type = "shipping_order"
            entities = annotate_shipping_order(pdf_path)
        else:
            console.print("[yellow]⚠ Unknown document type - please categorize[/yellow]")
            doc_type = Prompt.ask("Document type", choices=["invoice", "purchase_order", "shipping_order"])
            
            if doc_type == "invoice":
                entities = annotate_invoice(pdf_path)
            elif doc_type == "purchase_order":
                entities = annotate_purchase_order(pdf_path)
            else:
                entities = annotate_shipping_order(pdf_path)
        
        # Create annotation
        annotation = {
            "document_id": pdf_path.stem,
            "filename": pdf_path.name,
            "document_type": doc_type,
            "entities": entities,
            "annotation_metadata": {
                "annotated_date": datetime.now().isoformat(),
                "source_path": str(pdf_path.relative_to(data_path)),
                "annotator": "manual"
            }
        }
        
        # Save annotation
        relative_path = pdf_path.relative_to(data_path)
        annotation_path = output_path / relative_path.parent / f"{pdf_path.stem}.json"
        annotation_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(annotation_path, "w", encoding="utf-8") as f:
            json.dump(annotation, f, indent=2, ensure_ascii=False)
        
        console.print(f"\n[green]✓ Saved: {annotation_path.relative_to(Path.cwd())}[/green]")
        
        # Progress checkpoint
        remaining = len(unannotated) - i - 1
        if remaining > 0:
            console.print(f"[dim]({remaining} documents remaining)[/dim]")
            
            if not Confirm.ask("\n▶️  Continue to next document?", default=True):
                console.print(f"\n[yellow]⏸️  Paused. {remaining} documents remaining.[/yellow]")
                console.print(f"[cyan]Resume anytime: python scripts/annotate_documents.py --resume[/cyan]")
                break
    
    console.print("\n" + "="*60)
    console.print("[bold green]✓ Annotation session complete![/bold green]")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("1. Validate annotations: python scripts/validate_annotations.py")
    console.print("2. Split data: python scripts/split_data.py")

if __name__ == "__main__":
    main()
