"""Data schemas for document entities."""
from datetime import date
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# ============================================================
# BASE ENTITIES
# ============================================================

class AddressEntity(BaseModel):
    """Address information extracted from documents."""
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    full_address: Optional[str] = None  # Fallback for unparsed addresses

class CompanyEntity(BaseModel):
    """Company/organization information."""
    name: str
    address: Optional[AddressEntity] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None

class LineItemEntity(BaseModel):
    """Single line item in invoice or purchase order."""
    description: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    hs_code: Optional[str] = None  # Harmonized System code

class CargoItemEntity(BaseModel):
    """Cargo/shipment item for shipping orders."""
    description: str
    quantity: Optional[float] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = "kg"
    dimensions: Optional[str] = None
    package_type: Optional[str] = None

# ============================================================
# DOCUMENT-SPECIFIC ENTITIES
# ============================================================

class InvoiceEntity(BaseModel):
    """Commercial invoice document structure."""
    document_type: Literal["invoice"] = "invoice"
    invoice_number: str
    invoice_date: Optional[str] = None  # Changed from date to str for flexibility
    seller: Optional[CompanyEntity] = None
    buyer: Optional[CompanyEntity] = None
    line_items: List[LineItemEntity] = Field(default_factory=list)
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = "USD"
    payment_terms: Optional[str] = None
    due_date: Optional[str] = None
    notes: Optional[str] = None

class PurchaseOrderEntity(BaseModel):
    """Purchase order document structure."""
    document_type: Literal["purchase_order"] = "purchase_order"
    po_number: str
    po_date: Optional[str] = None
    buyer: Optional[CompanyEntity] = None
    supplier: Optional[CompanyEntity] = None
    line_items: List[LineItemEntity] = Field(default_factory=list)
    total: Optional[float] = None
    currency: Optional[str] = "USD"
    delivery_date: Optional[str] = None
    delivery_address: Optional[AddressEntity] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None

class ShippingOrderEntity(BaseModel):
    """Shipping order/bill of lading document structure."""
    document_type: Literal["shipping_order"] = "shipping_order"
    order_number: str
    ship_date: Optional[str] = None
    shipper: Optional[CompanyEntity] = None
    consignee: Optional[CompanyEntity] = None
    cargo_items: List[CargoItemEntity] = Field(default_factory=list)
    total_weight: Optional[float] = None
    weight_unit: Optional[str] = "kg"
    origin: Optional[str] = None
    destination: Optional[str] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    vessel_name: Optional[str] = None
    container_number: Optional[str] = None
    notes: Optional[str] = None

# ============================================================
# ANNOTATION WRAPPER
# ============================================================

class DocumentAnnotation(BaseModel):
    """Complete annotation for a document including metadata."""
    document_id: str
    filename: str
    document_type: Literal["invoice", "purchase_order", "shipping_order"]
    entities: InvoiceEntity | PurchaseOrderEntity | ShippingOrderEntity
    annotation_metadata: dict = Field(default_factory=dict)
    
    class Config:
        # Allow extra fields for future extensibility
        extra = "allow"
