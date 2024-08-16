from pydantic import BaseModel
from typing import Optional, List


class Bloge(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Bloge] = []

    class Config:
        orm_mode = True



class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True

class Login(BaseModel):
    email:str
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None