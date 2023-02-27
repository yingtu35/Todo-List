from typing import Union, Optional
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .utils import hash_password, verify_password
from .credentials import SECRET_KEY, ALORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from fastapi import Cookie, Response
from .models import User

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=[
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:3000"
]

# To allow cross-origin request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# TODO: Handle token expiration and redirect user to login page

async def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    return user

async def current_active_user(active_user: User = Depends(current_user)):
    if not active_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return active_user

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Hello World."}

@app.get("/items", tags=["todos"], status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    todos = user.todos
    return {"todos": todos}

@app.post("/items", tags=["todos"], status_code=status.HTTP_201_CREATED)
def create_item(body: schemas.TodoCreate, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user.id
    item = body.item
    newtodo = crud.create_item(db, user_id, item)
    return newtodo

@app.put("/items/{id}", tags=["todos"], status_code=status.HTTP_200_OK)
def update_item(id: int, body: schemas.TodoUpdate, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = queryset.first()
    if db_item.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    item = body.item
    crud.update_item(db, db_item, item)
    return True

@app.delete("/items/{id}", tags=["todos"], status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    queryset = db.query(models.Todo).filter(models.Todo.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")
    db_item = queryset.first()
    if db_item.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of the item")
    crud.delete_item(db, db_item)
    return

@app.get("/user", tags=["users"])
def get_user(db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"username": user.username,
                     "email": user.email,}}

@app.get("/users", tags=["users"], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Access denied")
    db_admin = crud.get_admin(db)
    if db_admin.id != user.id:
        raise HTTPException(status_code=401, detail="Access denied")
    users = crud.read_all_users(db)
    return {"users": users}

@app.delete("/users/{id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Access denied")
    db_admin = crud.get_admin(db)
    if db_admin.id != user.id:
        raise HTTPException(status_code=401, detail="Access denied")
    
    queryset = db.query(models.User).filter(models.User.id == id)
    if queryset.count() == 0:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    user_to_delete = queryset.first()

    crud.delete_user(db, user_to_delete)
    return

@app.put("/users", tags=["users"], status_code=status.HTTP_200_OK)
def update_user_password(body: schemas.UserUpdate, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    crud.update_user_password(db, user, body.new_password)
    return

@app.post("/signup", tags=["users"])
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
    return {"username": username}

@app.post("/login", tags=["users"], status_code=status.HTTP_200_OK)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = crud.verify_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    crud.update_is_active(db, user, True)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"username": username, 
            "access_token": access_token, 
            "token_type": "bearer"}

@app.post("/logout", tags=["users"], status_code=status.HTTP_200_OK) 
def user_logout(db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    crud.update_is_active(db, user, is_active=False)
    return

""" OAuth2 Authentication and Authorization"""
# tokenUrl is the URL the client use to send username and password to get a token

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALORITHM)
    return encoded_jwt


