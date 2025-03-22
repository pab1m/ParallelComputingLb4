from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str  # "client" або "admin"


users = []


@app.post("/users")
def create_user(user: UserCreate):
    users.append(user.dict())
    print(user.dict())
    return user


@app.get("/users")
def get_users():
    return users

