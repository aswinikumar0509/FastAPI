from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Library API")

class BookCreate(BaseModel):
    title: str
    author: str
    available_copies: int

class Book(BookCreate):
    id: int

class MemberCreate(BaseModel):
    name: str
    email: str

class Member(MemberCreate):
    id: int

class BorrowRecord(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrow_date: date
    return_date: Optional[date] = None

books: List[Book] = []
members: List[Member] = []
records: List[BorrowRecord] = []
next_book_id = 1
next_member_id = 1
next_record_id = 1

@app.post("/book", response_model=Book)
def add_book(data: BookCreate):
    global next_book_id
    book = Book(id=next_book_id, **data.dict())
    next_book_id += 1
    books.append(book)
    return book

@app.get("/books",response_model=List[Book])
def list_books():
    return books

@app.post("/members",response_model=Member)
def add_member(data:MemberCreate):
    global next_member_id
    member = Member(id=next_member_id,**data.dict())
    next_member_id+=1
    members.append(member)
    return member