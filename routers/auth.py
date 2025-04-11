# from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
# from pydantic import BaseModel
# from passlib.hash import bcrypt
# from jose import jwt
# import uuid
# import shutil

# router = APIRouter()

# # Simulated user DB
# fake_users_db = {}

# SECRET_KEY = "your-secret-key"

# class User(BaseModel):
#     id: str
#     email: str
#     name: str
#     password: str
#     phone: str = None
#     bio: str = ""
#     photo: str = ""

# def get_user_from_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return fake_users_db[payload["email"]]
#     except:
#         raise HTTPException(status_code=401, detail="Invalid token")

# @router.post("/register")
# def register(email: str = Form(), name: str = Form(), password: str = Form()):
#     if email in fake_users_db:
#         raise HTTPException(status_code=400, detail="Email exists")
#     uid = str(uuid.uuid4())
#     fake_users_db[email] = User(
#         id=uid, email=email, name=name, password=bcrypt.hash(password)
#     )
#     return {"msg": "User registered"}

# @router.post("/login")
# def login(email: str = Form(), password: str = Form()):
#     user = fake_users_db.get(email)
#     if not user or not bcrypt.verify(password, user.password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm="HS256")
#     return {"access_token": token}

# @router.get("/me")
# def me(token: str):
#     user = get_user_from_token(token)
#     return user

# @router.post("/edit")
# def edit_profile(
#     token: str,
#     name: str = Form(None),
#     bio: str = Form(None),
#     phone: str = Form(None),
#     email: str = Form(None),
#     password: str = Form(None),
# ):
#     user = get_user_from_token(token)
#     if name: user.name = name
#     if bio: user.bio = bio
#     if phone: user.phone = phone
#     if email: user.email = email
#     if password: user.password = bcrypt.hash(password)
#     fake_users_db[user.email] = user
#     return {"msg": "Profile updated"}

# @router.post("/upload-photo")
# def upload_photo(token: str, file: UploadFile = File(...)):
#     user = get_user_from_token(token)
#     path = f"static/{user.id}_{file.filename}"
#     with open(path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     user.photo = path
#     return {"msg": "Photo uploaded", "photo_url": path}

# @router.post("/google-login")
# def google_login(dummy_token: str = Form(...)):
#     # Simulated Google login — in real life, verify using authlib
#     fake_email = "google_user@example.com"
#     if fake_email not in fake_users_db:
#         uid = str(uuid.uuid4())
#         fake_users_db[fake_email] = User(
#             id=uid, email=fake_email, name="Google User", password="oauth"
#         )
#     token = jwt.encode({"email": fake_email}, SECRET_KEY, algorithm="HS256")
#     return {"access_token": token}

# @router.post("/logout")
# def logout():
#     return {"msg": "Token should be deleted client-side to log out"}

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, status
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from jose import jwt, JWTError
from uuid import uuid4
import shutil
from typing import Optional

router = APIRouter()

# Simulated user DB
fake_users_db: dict[str, "User"] = {}

# Constants
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


# -------------------- Models --------------------

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    password: str
    phone: Optional[str] = None
    bio: str = ""
    photo: str = ""


class TokenResponse(BaseModel):
    access_token: str


class MessageResponse(BaseModel):
    msg: str


# -------------------- Utility Functions --------------------

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_access_token(email: str) -> str:
    return jwt.encode({"email": email}, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email or email not in fake_users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return fake_users_db[email]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# -------------------- Routes --------------------

@router.post("/register", response_model=MessageResponse)
def register(
    email: EmailStr = Form(...),
    name: str = Form(...),
    password: str = Form(...)
):
    if email in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        id=str(uuid4()),
        email=email,
        name=name,
        password=hash_password(password)
    )
    fake_users_db[email] = user
    return {"msg": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    user = fake_users_db.get(email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return {"access_token": create_access_token(user.email)}


@router.get("/me", response_model=User)
def get_profile(token: str):
    return decode_token(token)


@router.post("/edit", response_model=MessageResponse)
def edit_profile(
    token: str,
    name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    password: Optional[str] = Form(None)
):
    user = decode_token(token)

    if name: user.name = name
    if bio: user.bio = bio
    if phone: user.phone = phone
    if password: user.password = hash_password(password)
    if email:
        # Update key if email changes
        fake_users_db.pop(user.email)
        user.email = email
        fake_users_db[email] = user
    else:
        fake_users_db[user.email] = user

    return {"msg": "Profile updated successfully"}


@router.post("/upload-photo", response_model=MessageResponse)
def upload_photo(token: str, file: UploadFile = File(...)):
    user = decode_token(token)
    file_path = f"static/{user.id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user.photo = file_path
    fake_users_db[user.email] = user
    return {"msg": "Photo uploaded successfully"}


@router.post("/google-login", response_model=TokenResponse)
def google_login(dummy_token: str = Form(...)):
    # Simulate Google user (normally you'd verify token here)
    email = "google_user@example.com"
    if email not in fake_users_db:
        user = User(
            id=str(uuid4()),
            email=email,
            name="Google User",
            password="oauth"
        )
        fake_users_db[email] = user
    return {"access_token": create_access_token(email)}


@router.post("/logout", response_model=MessageResponse)
def logout():
    # Token invalidation is client-side in stateless JWT auth
    
    return {"msg": "Logged out successfully. Remove token on client side."}
