from fastapi import FastAPI , HTTPExceptions, Header, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Blog API")

class User(BaseModel):
    username:str
    email:str

class PostCreate(BaseModel):
    title:str
    content:str

class Post(PostCreate):
    id:int
    author:str
    created_at:datetime


