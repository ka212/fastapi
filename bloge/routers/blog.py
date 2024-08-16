from fastapi import APIRouter, Depends, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import oauth2
import sqlite3
import schema

router = APIRouter()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True

class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    published: bool
    creator_id: Optional[int]

    class Config:
        orm_mode = True

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@router.post('/blog', status_code=status.HTTP_201_CREATED, response_model=ShowBlog, tags=['blogs'])
def create_blog(request: Blog, db: sqlite3.Connection = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    cursor = db.cursor()
    creator_id = 2
    cursor.execute("INSERT INTO blogs (title, body, published, creator_id) VALUES (?, ?, ?, ?)",
                   (request.title, request.body, request.published, creator_id))
    db.commit()

    cursor.execute("SELECT * FROM blogs WHERE id = ?", (cursor.lastrowid,))
    new_blog = cursor.fetchone()

    return dict(new_blog)

@router.get('/blog', response_model=List[ShowBlog], tags=['blogs'])
def all(db: sqlite3.Connection = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs")
    blogs = cursor.fetchall()

    return [dict(blog) for blog in blogs] 

@router.get('/blog/{id}', status_code=200, response_model=ShowBlog, tags=['blogs'],)
def show(id: int, response: Response, db: sqlite3.Connection = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs WHERE id = ?", (id,))
    blog = cursor.fetchone()

    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    return dict(blog)  

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: Blog, response: Response, db: sqlite3.Connection = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs WHERE id = ?", (id,))
    blog = cursor.fetchone()

    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    cursor.execute("UPDATE blogs SET title = ?, body = ?, published = ? WHERE id = ?", 
                   (request.title, request.body, request.published, id))
    db.commit()  
    return {"message": "Blog updated successfully."}

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id: int, response: Response, db: sqlite3.Connection = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs WHERE id = ?", (id,))
    blog = cursor.fetchone()

    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    cursor.execute("DELETE FROM blogs WHERE id = ?", (id,))
    db.commit()
    return {"message": "Blog deleted successfully."}
