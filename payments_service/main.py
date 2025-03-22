from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class PaymentCreate(BaseModel):
    id: int
    invoice_id: int
    method: str  # "card", "cash"
    status: str  # "pending", "successful", "failed"


payments = []


@app.post("/payments")
def create_payment(new_payment: PaymentCreate):
    payments.append(new_payment.dict())
    print(new_payment.dict())
    return new_payment


@app.get("/payments")
def get_payment():
    return payments

