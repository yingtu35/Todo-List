from typing import List
from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    item: str

class TodoCreate(TodoBase):
    owner_id: int

class TodoUpdate(TodoBase):
    owner_id: int

class TodoDelete(BaseModel):
    owner_id: int

class Todo(TodoBase):
    id: int
    createdAt: datetime
    owner_id: str


    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    todos: List[Todo]

    class Config:
        orm_mode = True