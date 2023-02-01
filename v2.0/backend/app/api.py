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

# make some changes

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Hello World."}

@app.get("/item/{user_id}", tags=["todos"], status_code=status.HTTP_200_OK)
def get_items(user_id: int, db: Session = Depends(get_db)):
    user = crud.read_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    todos = user.todos
    return {"todos": todos}

@app.post("/item", tags=["todos"], status_code=status.HTTP_201_CREATED)
def create_item(body: schemas.TodoCreate, db: Session = Depends(get_db)):
    newtodo = crud.post_user_item(db, body)
    return newtodo

@app.put("/item/{id}", tags=["todos"], status_code=status.HTTP_200_OK)
def update_item(id: int, body: schemas.TodoUpdate, db: Session = Depends(get_db)) -> dict:
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    if db_item.owner_id != body.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    item = body.item
    newTodo = crud.update_item(db, db_item, item)
    return {"Success": "Item {id} updated"}

@app.delete("/item/{id}", tags=["todos"])
def delete_item(id: int, body: schemas.TodoDelete, db: Session = Depends(get_db)) -> dict:
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    if db_item.owner_id != body.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    crud.delete_item(db, db_item)
    return {"Success": "Item {id} deleted"}

@app.get("/user/{id}", tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)) -> dict:
    user = crud.read_user(db, id)
    return {"user": {"email": user.email, "id": user.id}}

@app.get("/user", tags=["users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.read_user_by_email(db, email)
    return {"user": {"email": user.email, "id": user.id}}

@app.get("/users", tags=["users"], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = crud.read_all_users(db)
    return {"users": users}

# body will change to schemas.UserCreate in the future
# TODO: Include username to create a user account
@app.post("/user/create", tags=["users"])
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    email = body.email
    password = body.password

    query = db.query(models.User).filter(models.User.email == email)
    if query.count() != 0:
        raise HTTPException(status_code=400, detail="Email already been used")
    user = crud.post_user(db, email, password)
    user_id = user.id

    return {"message": "user is created",
            "user_id": user_id}

@app.post("/user/login", tags=["users"], status_code=status.HTTP_200_OK)
def user_login(body: schemas.UserLogin, db: Session = Depends(get_db)):
    email = body.email
    password = body.password

    isVerified, user = crud.verify_user(db, email, password)
    if not isVerified:
        raise HTTPException(status_code=400, detail="invalid email or password")

    user_id = user.id

    return {"message": "Login success",
            "user_id": user_id} 