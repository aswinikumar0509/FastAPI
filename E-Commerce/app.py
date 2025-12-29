from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="E-Commerce Core")

class User(BaseModel):
    username :str
    is_admin:bool=False

users:dict[str,User] = {
    "admin":User(username="admin",is_admin=True),
    "aswini":User(username="aswini",is_admin=False)
}

def get_current_user(x_user:Optional[str]=Header(None))->User:
    if not x_user or x_user not in users:
        raise HTTPException(status_code=401,details="X-User header required")
    return users[x_user]

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class Product(ProductCreate):
    id: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    id: int
    user: str
    items: List[OrderItem]
    total: float
    status: str = "created"

products: List[Product] = []
next_product_id = 1
carts: dict[str, List[CartItem]] = {}
orders: List[Order] = []
next_order_id = 1