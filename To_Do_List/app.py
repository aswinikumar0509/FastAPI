from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List,Optional

app = FastAPI(title="TO-DO-List API")

class TodoCreate(BaseModel):
    title:str
    completed:bool = False

class Todo(TodoCreate):
    id:int

todos:List[Todo] = []
next_id = 1

@app.post("/todos", response_model=Todo)
def create_todo(todo:TodoCreate):
    global next_id
    new = Todo(id=next_id,**todo.dict())
    next_id+=1
    todos.append(new)
    return new

@app.get("/todo", response_model=List[Todo])
def list_todos(completed:Optional[bool]=None):
    if completed is None:
        return todos
    return [t for t in todos if t.completed==completed]

@app.get("/todos/{todo_id}",response_model=Todo)
def get_todo(todo_id:int):
    for t in todos:
        if t.id==todo_id:
            return t
        
    raise HTTPException(status_code=404,detail="Todo not found")

@app.put("/todos/{todo_id}",response_model=Todo)
def update_todo(todo_id:int,data:TodoCreate):
    for i,t in enumerate(todos):
        if t.id==todo_id:
            updated = Todo(id=todo_id,**data.dict())
            todos[i]=updated
            return updated
    raise HTTPException(status_code=404,detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for i,t in enumerate(todos):
        if t.id==todo_id:
            todos.pop(i)
            return {"message":"Todo Deleted"}
        
    raise HTTPException(status_code=404,detail="Todo not found")

