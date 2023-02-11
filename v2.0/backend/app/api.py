from typing import Union, Optional
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .utils import hash_password, verify_password

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

# TODO: Should implement token to authorize actions
@app.get("/user", tags=["users"])
def get_user(db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"username": user.username,
                     "email": user.email,}}

# @app.get("/users/", tags=["users"])
# def get_user_by_email(email: str, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     user = crud.read_user_by_email(db, email)
#     return {"user": {"email": user.email, "id": user.id}}

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

# TODO: set_cookie method not working for localhost
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

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def hash_password(password):
#     return pwd_context.hash(password)

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# # automatically check the Authorization header
# @app.get("/test/")
# async def read_tokens(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

# class fake_User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None

# class fake_UserInDB(fake_User):
#     hashed_password: str

# def fake_hash_password(password: str):
#     return "fakehashed" + password

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return fake_UserInDB(**user_dict)

# # def fake_decode_token(token):
# #     # This doesn't provide any security at all
# #     # Check the next version
# #     user = get_user(fake_users_db, token)
# #     return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALORITHM)
    return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     return user

# async def get_current_active_user(active_user: fake_User = Depends(get_current_user)):
#     if active_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return active_user

# @app.get("/test/me")
# async def read_me(user: fake_User = Depends(get_current_active_user)):
#     return user



# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

SECRET_KEY = "871796f3497fd7ce65efd5d475c794a4723d2907b3c2b3730ca838070ca816d3"
ALORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenDate(BaseModel):
#     username: Union[str, None] = None


