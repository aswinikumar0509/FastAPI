from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from collections import defaultdict

app = FastAPI(title="Expense Tracker")

class ExpenseCreate(BaseModel):
    amount:float
    category:str
    description: Optional[str] = None
    date:date

class Expense(ExpenseCreate):
    id: int

expenses : List[Expense] = []
next_id = 1

@app.post("/expenses",response_model=Expense)
def add_expense(data:ExpenseCreate):
    global next_id
    exp = Expense(id=next_id,**data.dict())
    next_id+=1
    expenses.append(exp)
    return exp

@app.get("/expenses",response_model=List[Expense])
def list_expense(category:Optional[str]=None,date_from:Optional[str]=None,date_to:Optional[date]=None):
    result = expenses
    if category:
        result = [e for e in result if e.category==category]
    if date_from:
        result = [e for e in result if e.date >= date_from]
    if date_to:
        result = [e for e in result if e.date <= date_to]

    return result

@app.get("/expenses/summary")
def summary_by_category():
    totals = defaultdict(float)
    for e in expenses:
        totals[e.category]+=e.amount
    return [{"category":c ,"total":t} for c,t in totals.items]