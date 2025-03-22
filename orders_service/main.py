from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

orders = []


class Order(BaseModel):
    id: int
    user_id: int
    items: List[dict]
    status: str  # "pending", "confirmed"


@app.post("/orders")
def create_order(order: Order):
    orders.append(order.dict())
    print(order.dict())
    return order


@app.get("/orders")
def get_orders():
    return orders


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    orders.remove(order)
    return None


@app.put("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order["status"] = "confirmed"
    return order

