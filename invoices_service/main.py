from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class InvoiceCreate(BaseModel):
    id: int
    order_id: int
    amount: float
    is_paid: bool


invoices = []


@app.post("/invoices")
def create_invoice(invoice: InvoiceCreate):
    invoices.append(invoice.dict())
    print(invoice.dict())
    return invoice


@app.get("/invoices")
def get_invoice():
    return invoices

