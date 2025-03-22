import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

ORDERS_SERVICE_URL = "http://orders_service:8002/orders"
MENU_SERVICE_URL = "http://menu_service:8003/menu"


class InvoiceCreate(BaseModel):
    id: int
    order_id: int
    amount: float
    is_paid: bool


invoices = []


@app.get("/invoices")
def get_invoice():
    return invoices


@app.post("/orders/{order_id}/invoice", response_model=InvoiceCreate)
def create_invoice(order_id: int):
    # Отримуємо замовлення з зовнішнього сервісу Orders
    order_response = requests.get(f"{ORDERS_SERVICE_URL}/{order_id}")
    if order_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Order not found")
    order = order_response.json()

    # Отримуємо меню з зовнішнього сервісу Menu
    menu_response = requests.get(f"{MENU_SERVICE_URL}")
    if menu_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Menu service unavailable")
    menu = menu_response.json()

    # Перевіряємо, чи всі пункти меню існують
    for item in order["items"]:
        if not any(m["id"] == item["menu_id"] for m in menu):
            raise HTTPException(
                status_code=400,
                detail=f"Menu item with ID {item['menu_id']} not found"
            )

    # Обчислюємо загальну вартість
    total_price = sum(
        item["quantity"] * next((m["price"] for m in menu if m["id"] == item["menu_id"]), 0)
        for item in order["items"]
    )

    # Створюємо нову накладну
    new_invoice = InvoiceCreate(id=len(invoices) + 1, order_id=order_id, amount=total_price, is_paid=False)
    invoices.append(new_invoice)
    return new_invoice