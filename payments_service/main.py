import json
import redis
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Підключення до Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


class PaymentCreate(BaseModel):
    id: int
    invoice_id: int
    method: str  # "card", "cash"
    status: str  # "pending", "successful", "failed"


payments = []


@app.post("/payments")
def create_payment(new_payment: PaymentCreate):
    payments.append(new_payment.dict())
    redis_client.set("payments", json.dumps(payments))
    assert redis_client.get("payments") is not None
    return new_payment


@app.get("/payments")
def get_payment():
    cached_payments = redis_client.get("payments")
    if cached_payments:
        return json.loads(cached_payments)
    redis_client.setex("payments", 60, json.dumps(payments))  # Кешуємо меню на 60 секунд
    return payments

