from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from datetime import datetime

# left for future extension
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

def getCurrentTime():
    return datetime.now()
    

class Todo(Base):
    __tablename__ = "todos"

    id = Column("id", Integer, primary_key=True, index=True)
    item = Column("item", String, index=True)
    createdAt = Column("createdAt", DateTime, default=getCurrentTime)
    # owner = Column("owner", String)