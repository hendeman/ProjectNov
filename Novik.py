import uvicorn
from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="TrApp")

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob", "age": 20},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Leonid", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"},
    ]},
    {"id": 4, "role": "trader", "name": "Leonid", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "LOL"},
    ]},

]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_name": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_name": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


@app.get("/trades")
def get_user(limit: int = 1, offset: int = 2):
    return fake_trades[offset:][:limit]


fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Leonid"},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trade(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
