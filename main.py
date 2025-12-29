from typing import List

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field, field_validator

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="DataBridge AI",
    version="1.0.0",
    description="Invoice parsing API (mock mode)"
)

# =========================
# PYDANTIC SCHEMAS
# =========================

class InvoiceLineItem(BaseModel):
    description: str = Field(..., description="Product or service name")
    quantity: float = Field(gt=0, description="Quantity must be > 0")
    unit_price: float = Field(gt=0, description="Unit price must be > 0")
    total: float = Field(gt=0)

    @field_validator("total")
    @classmethod
    def validate_total(cls, v, info):
        qty = info.data.get("quantity", 0)
        price = info.data.get("unit_price", 0)
        expected = qty * price
        if abs(v - expected) > 0.01:
            raise ValueError(f"total mismatch: {v} != {expected}")
        return v


class Invoice(BaseModel):
    invoice_number: str
    date: str = Field(..., description="YYYY-MM-DD")
    vendor_name: str
    total_amount: float
    currency: str = Field(default="EUR", pattern=r"^[A-Z]{3}$")
    line_items: List[InvoiceLineItem]

# =========================
# ENDPOINTS
# =========================

@app.get("/health")
def health():
    return {
        "status": "operational",
        "mode": "mock"
    }


@app.post("/parse/invoice", response_model=Invoice)
async def parse_invoice(file: UploadFile = File(...)):
    """
    MOCK MODE
    Simula il parsing di una fattura e restituisce JSON realistico.
    Non usa OpenAI.
    """

    # Leggiamo il file solo per coerenza (non lo usiamo)
    await file.read()

    return Invoice(
        invoice_number="INV-2024-001",
        date="2024-05-12",
        vendor_name="ACME SRL",
        total_amount=123.45,
        currency="EUR",
        line_items=[
            InvoiceLineItem(
                description="Servizio di consulenza",
                quantity=1,
                unit_price=123.45,
                total=123.45
            )
        ]
    )
