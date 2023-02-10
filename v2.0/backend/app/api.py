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

    # TODO: should check user based on their tokens or session cookie
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

    # TODO: should check user based on their tokens or session cookie
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

    crud.update_is_active(db, user, True)
    user_id = user.id

    return {"username": username, "user_id": user_id}

@app.post("/logout", tags=["users"], status_code=status.HTTP_200_OK) 
def user_logout(body: schemas.UserLogout, db: Session = Depends(get_db)):
    username = body.username
    queryset = db.query(models.User).filter(models.User.username == username)
    if queryset.count() == 0:
        return HTTPException(status_code=400, detail="Invalid username")

    # TODO: should check user based on their tokens or session cookie
    db_user = queryset.first()

    crud.update_is_active(db, db_user, False)
    return

"""Cookie test"""
@app.get("/set")
async def set_cookie(response: Response):
    response.set_cookie(key="refresh_token", value="username", max_age=300)
    return True

@app.get("/get")
async def get_cookie(refresh_token: Optional[str] = Cookie(None)):
    print(refresh_token)
    return True


""" OAuth2 Authentication and Authorization"""
# tokenUrl is the URL the client use to send username and password to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# automatically check the Authorization header
@app.get("/test/")
async def read_tokens(token: str = Depends(oauth2_scheme)):
    return {"token": token}

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class fake_User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class fake_UserInDB(fake_User):
    hashed_password: str

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return fake_UserInDB(**user_dict)

# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(fake_users_db, username=token_data.username)
    return user

async def get_current_active_user(active_user: fake_User = Depends(get_current_user)):
    if active_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return active_user

@app.get("/test/me")
async def read_me(user: fake_User = Depends(get_current_active_user)):
    return user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

SECRET_KEY = "871796f3497fd7ce65efd5d475c794a4723d2907b3c2b3730ca838070ca816d3"
ALORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenDate(BaseModel):
#     username: Union[str, None] = None


