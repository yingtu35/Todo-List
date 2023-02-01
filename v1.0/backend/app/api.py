from typing import Union
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=[
    "http://localhost:3000",
    "localhost:3000"
]

# To allow cross-origin request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Hello World."}

@app.get("/item", tags=["todos"], status_code=status.HTTP_200_OK)
def get_item(db: Session = Depends(get_db)):
    todos = crud.read_items(db)
    return {"todos": todos}

@app.post("/item", tags=["todos"], response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_item(body: schemas.TodoCreate, db: Session = Depends(get_db)):
    newtodo = crud.post_item(db, body)
    return newtodo

@app.put("/item/{id}", tags=["todos"], status_code=status.HTTP_200_OK)
def update_item(id: int, body: schemas.TodoUpdate, db: Session = Depends(get_db)) -> dict:
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    newTodo = crud.update_item(db, db_item, body)
    return {"Success": "Item {id} updated"}

@app.delete("/item/{id}", tags=["todos"])
def delete_item(id: int, db: Session = Depends(get_db)) -> dict:
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    crud.delete_item(db, db_item)
    return {"Success": "Item {id} deleted"}