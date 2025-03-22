from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

orders = []


class Order(BaseModel):
    id: int
    user_id: int
    items: List[dict]
    status: str  # "pending", "confirmed", "cooking", "completed"


@app.post("/orders")
def create_order(order: Order):
    orders.append(order.dict())
    print(order.dict())
    return order


@app.get("/orders")
def get_orders():
    return orders
