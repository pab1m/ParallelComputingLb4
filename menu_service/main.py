from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


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
    return items


@app.get("/menu/{menu_id}")
def get_menu_item(menu_id: int):
    item = next((i for i in items if i["id"] == menu_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@app.delete("/menu/{menu_id}")
def delete_menu(menu_id: int):
    mn = next((m for m in items if m["id"] == menu_id), None)
    if mn is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    items.remove(mn)
    return None
