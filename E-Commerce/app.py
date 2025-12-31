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

# products
@app.post("/products", response_model=Product)
def add_product(data: ProductCreate, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    global next_product_id
    p = Product(id=next_product_id, **data.dict())
    next_product_id += 1
    products.append(p)
    return p


@app.get("/products",response_model=List[Product])
def list_products(q:Optional[str]=None):
    if not q:
        return products
    q=q.lower()
    return [p for p in products if q in p.name.lower()]


### Cart

@app.post("/cart/add")
def cart_add(item:CartItem,user:User=Depends(get_current_user)):
    cart = carts.setdefault(user.username,[])
    for ci in cart:
        if ci.product_id==item.product_id:
            ci.quantity+=item.quantity
            break
        else:
            cart.append(item)
    return {"message":"Added to cart "}


@app.get("/cart",response_model=List[CartItem])
def cart_view(user:User=Depends(get_current_user)):
    return carts.get(user.username,[])

@app.delete("/cart/remove/{product_id}")
def cart_remove(product_id: int, user: User = Depends(get_current_user)):
    cart = carts.get(user.username, [])
    carts[user.username] = [ci for ci in cart if ci.product_id != product_id]
    return {"message": "Removed"}

# orders
@app.post("/orders", response_model=Order)
def create_order(user: User = Depends(get_current_user)):
    global next_order_id
    cart = carts.get(user.username, [])
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_items: List[OrderItem] = []
    total = 0.0

    for ci in cart:
        prod = next((p for p in products if p.id == ci.product_id), None)
        if not prod:
            raise HTTPException(status_code=400, detail="Product not found")
        if prod.stock < ci.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        prod.stock -= ci.quantity
        oi = OrderItem(product_id=prod.id, quantity=ci.quantity, price=prod.price)
        order_items.append(oi)
        total += oi.price * oi.quantity

    order = Order(
        id=next_order_id,
        user=user.username,
        items=order_items,
        total=total,
        status="created"
    )
    next_order_id += 1
    orders.append(order)
    carts[user.username] = []
    return order

@app.get("/orders", response_model=List[Order])
def list_orders(user: User = Depends(get_current_user)):
    if user.is_admin:
        return orders
    return [o for o in orders if o.user == user.username]