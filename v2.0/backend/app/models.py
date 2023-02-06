from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base
from datetime import datetime

def getCurrentTime():
    return datetime.now()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    createdAt = Column("createdAt", DateTime, default=getCurrentTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    todos = relationship("Todo", back_populates="owner")



    

class Todo(Base):
    __tablename__ = "todos"

    id = Column("id", Integer, primary_key=True, index=True)
    item = Column("item", String, index=True)
    createdAt = Column("createdAt", DateTime, default=getCurrentTime)
    owner_id = Column("owner_id", Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")