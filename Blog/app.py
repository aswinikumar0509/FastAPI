from fastapi import FastAPI, HTTPException, Header, Depends
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

users : dict[str,User] = {}
posts : List[Post] = []
next_post_id = 1

@app.post("/auth/register",response_model = User)
def register(user:User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username taken")
    users[user.username]= user
    return user

def get_current_user(x_user:Optional[str]=Header(None))->User:
    if not x_user or x_user not in users:
        raise HTTPException(status_code=401,detail="X_user Header required")
    return users[x_user]


@app.post("/Posts",response_model=Post)
def create_post(data:PostCreate,user:User = Depends(get_current_user)):
    global next_post_id
    post = Post(
        id = next_post_id,
        title=data.title,
        content=data.content,
        author=user.username,
        created_at=datetime.utcnow()
    )
    next_post_id+=1
    posts.append(post)
    return post

@app.get("/posts",response_model=List[Post])
def list_posts(page:int=1,size:int=5):
    start = (page-1)*size
    end = start+size
    return posts[start:end]

@app.get("/posts/{post_id}",response_model=Post)
def get_post(post_id:int):
    for  i in posts:
        if i.id==post_id:
            return i
    raise HTTPException(status_code=404,detail=" Post not found ")

@app.put("/posts/{post_id}" , response_model=Post)
def update_post(post_id:int,data:PostCreate,user:User=Depends(get_current_user)):
    for i , p in enumerate(posts):
        if p.id == post_id:
            if p.author!=user.username:
                raise HTTPException(status_code=403,detail="Not your post")
            updated = Post(
                id=p.id,
                title=data.title,
                content=data.content,
                author=p.author,
                created_at=p.created_at
            )
            posts[i]=updated
            return updated
        
    raise HTTPException(status_code=404,detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id:int,user:User=Depends(get_current_user)):
    for i,p in enumerate(posts):
        if p.id==post_id:
            if p.author not in user.username:
                raise HTTPException(status_code=403,detail="Not you post")
            posts.pop(i)
            return {"message":"Post Deleted"}
        
    raise HTTPException(status_code=404,detail="Post not found ")
