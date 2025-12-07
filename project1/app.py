from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:str

app = FastAPI()

@app.get("/hello")
def say_hello(name:str):
    return {"message":f"Hello {name}"}

@app.get("/add")
def add(a:int,b:int):
    return {"result":a+b}


@app.post("/user")
def create_user(user:User):
    return {"status":"created","user":user}

# "========================================================"

items = []

class Item(BaseModel):
    id:int
    name:str

@app.post("/items")
def add_item(item:Item):
    items.append(item)
    return {"message":"Item Added"}

@app.get("/items")
def get_item():
    return items

@app.get("/items/{id}")
def get_item(id:int):
    for item in items:
        if item.id==id:
            return item
    return {"error":"Item not found"}

@app.delete("/items/{id}")
def delete_item(id:int):
    global items
    items = [item for item in items if item.id != id]
    return {"message":"item get deleted"}