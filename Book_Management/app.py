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

@app.post("/borrow",response_model=BorrowRecord)
def borrow_book(book_id:int, member_id:int):
    global next_record_id
    book = next((b for b in books if b.id==book_id), None)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    if book.available_copies<1:
        raise HTTPException(status_code=400,detail="No copies avaliable")
    member = next((m for m in member if m.id==member_id), None)
    if not member:
        raise HTTPException(status_code=404,detail="Memeber not found")
    
    book.available_copies-=1

    record=BorrowRecord(
        id=next_record_id,
        book_id=book_id,
        member_id=member_id,
        borrow_date = date.today()
    )

    next_record_id+=1
    records.append(record)
    return record

@app.post("/return",response_model=BorrowRecord)
def return_book(record_id:int):
    record = next((r for r in records if r.id==record_id ), None)
    if not record:
        raise HTTPException(status_code=404,detail="Record not found")
    if record.return_date is not None:
        raise HTTPException(status_code=400,detail="Already returned")
    record.return_date = date.today()
    book = next((b for b in books if b.id==record.book_id), None)
    if book:
        book.available_copies+=1
    return record

@app.get("/records/overdue",response_model=List[BorrowRecord])
def overdue(days:int=15):
    today = date.today()
    result = []
    for r in records:
        if r.return_date is None:
            delta = (today-r.borrow_date).days
            if delta>days:
                result.append(r)

    return result