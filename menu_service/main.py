from fastapi import FastAPI
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

