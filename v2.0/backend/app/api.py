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

@app.get("/items/user/{user_id}", tags=["todos"], status_code=status.HTTP_200_OK)
def get_items(user_id: int, db: Session = Depends(get_db)):
    user = crud.read_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    todos = user.todos
    return {"todos": todos}

@app.post("/items/user/{user_id}", tags=["todos"], status_code=status.HTTP_201_CREATED)
def create_item(body: schemas.TodoCreate, db: Session = Depends(get_db)):
    newtodo = crud.post_user_item(db, body)
    return newtodo

@app.put("/items/{id}", tags=["todos"], status_code=status.HTTP_200_OK)
def update_item(id: int, body: schemas.TodoUpdate, db: Session = Depends(get_db)) -> dict:
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    if db_item.owner_id != body.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    item = body.item
    crud.update_item(db, db_item, item)
    return {"Success": "Item {id} updated"}

@app.delete("/items/{id}", tags=["todos"], status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, body: schemas.TodoDelete, db: Session = Depends(get_db)):
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item {id} not found")
    db_item = queryset.first()
    if db_item.owner_id != body.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    crud.delete_item(db, db_item)
    return

# TODO: Should implement token to authorize actions
@app.get("/users/{id}", tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)) -> dict:
    user = crud.read_user(db, id)
    return {"user": {"email": user.email, "id": user.id}}

@app.get("/users/", tags=["users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.read_user_by_email(db, email)
    return {"user": {"email": user.email, "id": user.id}}

@app.get("/users", tags=["users"], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = crud.read_all_users(db)
    return {"users": users}

@app.delete("/users/{id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, body: schemas.UserDelete, db: Session = Depends(get_db)):
    username = body.username
    password = body.password

    db_admin = crud.get_admin(db)
    _, db_user = crud.verify_user(db, username, password)
    if db_user is None or db_admin.id != db_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    queryset = db.query(models.User).filter(models.User.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="User {id} not found")

    crud.delete_user(db, db_user)
    return

@app.put("/users/{id}", tags=["users"], status_code=status.HTTP_200_OK)
def update_user(id: int, body: schemas.UserUpdate, db: Session = Depends(get_db)):
    username = body.username
    new_username = body.new_username
    password = body.password

    isVerified, db_user = crud.verify_user(db, username, password)
    if not isVerified or db_user.id != id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    crud.update_user(db, db_user, new_username)
    return

@app.post("/Sign-up", tags=["users"])
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    username = body.username
    email = body.email
    password = body.password

    query = db.query(models.User).filter(models.User.email == email)
    if query.count() != 0:
        raise HTTPException(status_code=400, detail="Email already been used")
    query = db.query(models.User).filter(models.User.username == username)
    if query.count() != 0:
        raise HTTPException(status_code=400, detail="Username already been used")
    
    user = crud.post_user(db, username, email, password)
    user_id = user.id

    return {"username": username, "user_id": user_id}

@app.post("/login", tags=["users"], status_code=status.HTTP_200_OK)
def user_login(body: schemas.UserLogin, db: Session = Depends(get_db)):
    username = body.username
    password = body.password

    isVerified, user = crud.verify_user(db, username, password)
    if not isVerified:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_id = user.id

    return {"username": username, "user_id": user_id}

# TODO: logout set user's is_active to false
# @app.post("/logout") 