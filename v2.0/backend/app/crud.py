from sqlalchemy.orm import Session, Query
from .models import User, Todo

from . import schemas
from .utils import hash_password, verify_password

def read_user_items(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def post_user_item(db: Session, body: schemas.TodoCreate):
    db_item = Todo(**body.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Todo, item: str):
    db_item.item = item
    db.commit()
    db.refresh(db_item)
    return

def delete_item(db: Session, db_item: Todo):
    db.delete(db_item)
    db.commit()
    return

def read_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def read_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def read_all_users(db: Session):
    return db.query(User).all()

def delete_user(db: Session, db_user: Query):
    db.delete(db_user)
    db.commit()
    return

def update_user(db: Session, db_user: User, new_username: str):
    db_user.username = new_username
    db.commit()
    db.refresh(db_user)
    return

def post_user(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        return (False, None)
    
    hashed_password = db_user.hashed_password
    if not verify_password(password, hashed_password):
        return (False, None)
    return (True, db_user)

def get_admin(db: Session) -> User:
    db_admin = db.query(User).filter(User.id == 1).first()
    return db_admin

def update_is_active(db: Session, user: User, is_active: bool):
    user.is_active = is_active
    db.commit()
    return