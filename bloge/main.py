from fastapi import FastAPI
from routers import blog, users, authentication 
from database import get_db 
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            published BOOLEAN NOT NULL DEFAULT 1,
            creator_id INTEGER,
            FOREIGN KEY (creator_id) REFERENCES user(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

app.include_router(blog.router)
app.include_router(users.router)
app.include_router(authentication.router)

