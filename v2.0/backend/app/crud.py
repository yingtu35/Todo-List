from sqlalchemy.orm import Session, Query

from . import models, schemas
from .utils import hash_password, verify_password

def read_user_items(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def post_user_item(db: Session, body: schemas.TodoCreate):
    db_item = models.Todo(**body.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Query, item: str):
    db_item.item = item
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item: Query):
    db.delete(db_item)
    db.commit()
    return

def read_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def read_all_users(db: Session):
    return db.query(models.User).all()

# TODO: Include username to create a user account
def post_user(db: Session, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return (False, None)
    
    hashed_password = db_user.hashed_password
    if not verify_password(password, hashed_password):
        return (False, None)
    return (True, db_user)
