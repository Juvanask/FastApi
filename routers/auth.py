from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import jwt
import uuid
import shutil

router = APIRouter()

# Simulated user DB
fake_users_db = {}

SECRET_KEY = "your-secret-key"

class User(BaseModel):
    id: str
    email: str
    name: str
    password: str
    phone: str = None
    bio: str = ""
    photo: str = ""

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return fake_users_db[payload["email"]]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register")
def register(email: str = Form(), name: str = Form(), password: str = Form()):
    if email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email exists")
    uid = str(uuid.uuid4())
    fake_users_db[email] = User(
        id=uid, email=email, name=name, password=bcrypt.hash(password)
    )
    return {"msg": "User registered"}

@router.post("/login")
def login(email: str = Form(), password: str = Form()):
    user = fake_users_db.get(email)
    if not user or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}

@router.get("/me")
def me(token: str):
    user = get_user_from_token(token)
    return user

@router.post("/edit")
def edit_profile(
    token: str,
    name: str = Form(None),
    bio: str = Form(None),
    phone: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
):
    user = get_user_from_token(token)
    if name: user.name = name
    if bio: user.bio = bio
    if phone: user.phone = phone
    if email: user.email = email
    if password: user.password = bcrypt.hash(password)
    fake_users_db[user.email] = user
    return {"msg": "Profile updated"}

@router.post("/upload-photo")
def upload_photo(token: str, file: UploadFile = File(...)):
    user = get_user_from_token(token)
    path = f"static/{user.id}_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user.photo = path
    return {"msg": "Photo uploaded", "photo_url": path}

@router.post("/google-login")
def google_login(dummy_token: str = Form(...)):
    # Simulated Google login — in real life, verify using authlib
    fake_email = "google_user@example.com"
    if fake_email not in fake_users_db:
        uid = str(uuid.uuid4())
        fake_users_db[fake_email] = User(
            id=uid, email=fake_email, name="Google User", password="oauth"
        )
    token = jwt.encode({"email": fake_email}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}

@router.post("/logout")
def logout():
    return {"msg": "Token should be deleted client-side to log out"}