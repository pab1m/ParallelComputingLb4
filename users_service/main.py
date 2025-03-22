from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


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


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return None


