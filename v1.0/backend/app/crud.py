from sqlalchemy.orm import Session, Query

from . import models, schemas

def read_items(db: Session):
    return db.query(models.Todo).all()

def post_item(db: Session, body: schemas.TodoCreate):
    db_item = models.Todo(item=body.item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Query, body: schemas.TodoUpdate):
    db_item.item = body.item
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item: Query):
    db.delete(db_item)
    db.commit()
    return
