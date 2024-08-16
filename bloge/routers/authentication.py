from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from fastapi.security import OAuth2PasswordRequestForm
import hashing
import auth_token
from database import get_db  
from schema import Login, Token



router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM user WHERE email = ?", (request.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    if not hashing.Hash.verify(request.password, user['password']):  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")
    user_email = user['email']
    access_token = auth_token.create_access_token(data={"sub": user_email})

    return {"access_token": access_token, "token_type": "bearer"}
