from fastapi import APIRouter, Depends, status, Response, HTTPException
from pydantic import BaseModel
import sqlite3
import hashing

router = APIRouter()

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@router.post('/user', response_model=ShowUser, tags=['users'])
def create_user(request: User, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    hashed_password = hashing.Hash.bcrypt(request.password)
    cursor.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
                   (request.name, request.email, hashed_password))
    db.commit()

    cursor.execute("SELECT * FROM user WHERE id = ?", (cursor.lastrowid,))
    new_user = cursor.fetchone()

    return dict(new_user)

@router.get('/user/{id}', status_code=200, response_model=ShowUser, tags=['users'])
def show_user(id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE id = ?", (id,))
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")

    return dict(user)
