import json
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Підключення до Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


class Order(BaseModel):
    id: int
    user_id: int
    items: List[dict]
    status: str  # "pending", "confirmed"


orders = []


@app.post("/orders")
def create_order(order: Order):
    orders.append(order.dict())
    redis_client.set("orders", json.dumps(orders))
    assert redis_client.get("orders") is not None
    return order


@app.get("/orders")
def get_orders():
    cached_orders = redis_client.get("orders")
    if cached_orders:
        return json.loads(cached_orders)
    redis_client.setex("orders", 60, json.dumps(orders))  # Кешуємо меню на 60 секунд
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

