import json
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Підключення до Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


class MenuItemCreate(BaseModel):
    id: int
    name: str
    price: float
    description: str


items = []


@app.post("/menu")
def create_menu(item: MenuItemCreate):
    items.append(item.dict())
    print(item.dict())
    return item


@app.get("/menu")
def get_menu():
    cached_menu = redis_client.get("menu")
    if cached_menu:
        return json.loads(cached_menu)
    redis_client.setex("menu", 60, json.dumps(items))  # Кешуємо меню на 60 секунд
    redis_client.set("menu", json.dumps(items))
    assert redis_client.get("menu") is not None
    return items


@app.get("/menu/{menu_id}")
def get_menu_item(menu_id: int):
    cached_item = redis_client.get(f"menu_item_{menu_id}")
    if cached_item:
        return json.loads(cached_item)
    item = next((i for i in items if i["id"] == menu_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    redis_client.setex(f"menu_item_{menu_id}", 60, json.dumps(item))  # Кешуємо на 60 сек
    return item


@app.delete("/menu/{menu_id}")
def delete_menu(menu_id: int):
    mn = next((m for m in items if m["id"] == menu_id), None)
    if mn is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    items.remove(mn)
    return None
