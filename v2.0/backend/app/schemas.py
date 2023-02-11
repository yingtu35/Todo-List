from typing import List
from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    item: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    createdAt: datetime
    owner_id: str


    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str

class UserDelete(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str
    new_password: str

class UserLogin(UserBase):
    password: str

class UserLogout(UserBase):
    pass

class User(UserBase):
    id: str
    email: str
    todos: List[Todo]

    class Config:
        orm_mode = True