from fastapi import FastAPI, HTTPException
from pydantic import Basemodel
from typing import List, Optional
from datetime import date
from collections import defaultdict

app = FastAPI(title="Expense Tracker")

class ExpenseCreate(Basemodel):
    amount:float
    category:str
    description: Optional[str] = None
    date:date

class Expense(ExpenseCreate):
    id: int

expenses : List[Expense] = []
next_id = 1

