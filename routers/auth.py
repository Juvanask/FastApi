from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import jwt
import uuid
import shutil
import os  # ✅ Required for os.makedirs

router = APIRouter()

# Simulated user DB
fake_users_db = {}

# Add a default user for token testing (email: "string")
fake_users_db["string"] = {
    "id": str(uuid.uuid4()),
    "email": "string",
    "name": "Test User",
    "password": bcrypt.hash("test123"),
    "phone": "1234567890",
    "bio": "This is a test user.",
    "photo": ""
}

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
        user_data = fake_users_db[payload["email"]]
        return User(**user_data.dict()) if isinstance(user_data, User) else User(**user_data)
    except Exception as e:
        print(f"TOKEN ERROR: {e}")
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

@router.post("/upload-photo")  # ✅ Fixed: changed from @app to @router
def upload_photo(file: UploadFile = File(...), token: str = ""):
    user = get_user_from_token(token)

    os.makedirs("static", exist_ok=True)  # ✅ Ensure folder exists

    path = f"static/{user.id}_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update user profile with photo path
    user.photo = path
    fake_users_db[user.email] = user
    return {"msg": "Photo uploaded", "photo_url": path}

@router.post("/google-login")
def google_login(dummy_token: str = Form(...)):
    # Simulated Google login
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
