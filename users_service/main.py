import json
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Підключення до Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


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
    redis_client.set("users", json.dumps(users))
    assert redis_client.get("users") is not None  # Переконуємося, що кеш оновився
    return user


@app.get("/users")
def get_users():
    cached_users = redis_client.get("users")
    if cached_users:
        return json.loads(cached_users)
    redis_client.setex("users", 60, json.dumps(users))  # Кешуємо меню на 60 секунд
    return users


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return None


