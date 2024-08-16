from fastapi import FastAPI, Depends 
from schema import Bloge
import sqlite3
from typing import Optional
from pydantic import BaseModel
import sqlite3

def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS blogs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        published BOOLEAN NOT NULL DEFAULT 1)''')
    conn.commit()
    conn.close()

init_db()


def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row  
    try:
        yield conn
    finally:
        conn.close()

app = FastAPI()

@app.get('/blog')
def index(limit=10, published: bool=True, sort: Optional[str]=None, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    if published:
        cursor.execute(f"SELECT * FROM blogs WHERE published=1 LIMIT {limit}")
    else:
        cursor.execute(f"SELECT * FROM blogs LIMIT {limit}")
    blogs = cursor.fetchall()
    return {'data': [dict(blog) for blog in blogs]}

@app.get('/blog/unpublished')
def unpublished(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs WHERE published=0")
    blogs = cursor.fetchall()
    return {'data': [dict(blog) for blog in blogs]}

@app.get('/blog/{id}')
def show(id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blogs WHERE id=?", (id,))
    blog = cursor.fetchone()


@app.get('/blog/{id}/comments')
def comments(id: int, limit=10, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM comments WHERE blog_id=? LIMIT {limit}", (id,))
    comments = cursor.fetchall()
    return {'data': [dict(comment) for comment in comments]}


# Run the application
#if __name__== "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=9000)
