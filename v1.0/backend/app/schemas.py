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
    # owner: str

    class Config:
        orm_mode = True