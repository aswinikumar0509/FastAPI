from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Library API")

class BookCreate(BaseModel):
    title:str
    author:str
    available_copies:int

class Book(BookCreate):
    int:id

class MemberCreate(BaseModel):
    name:str
    email:str

class Member(MemberCreate):
    id:int

class BorrowRecord(BaseModel):
    id:int
    book_id:int
    member_id:int
    borrow_date:date
    return_date:Optional[date]=None

books: List[Book] = []
members: List[Member] = []
records: List[BorrowRecord] = []
next_book_id = 1
next_member_id = 1
next_record_id = 1