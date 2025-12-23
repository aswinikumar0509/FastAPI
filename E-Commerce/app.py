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

