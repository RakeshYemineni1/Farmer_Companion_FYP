from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from backend.db.mongo_database import get_db
from backend.core.security import hash_password, verify_password, create_access_token
from backend.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    language: str = "en"


class LoginRequest(BaseModel):
    username: str
    password: str


class LanguageUpdate(BaseModel):
    language: str


@router.post("/register")
async def register(body: RegisterRequest):
    db = get_db()
    if await db.users.find_one({"username": body.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await db.users.find_one({"email": body.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    await db.users.insert_one({
        "username": body.username,
        "email": body.email,
        "password_hash": hash_password(body.password),
        "language": body.language,
        "created_at": datetime.utcnow(),
    })
    return {"message": "Registered successfully"}


@router.post("/login")
async def login(body: LoginRequest):
    db = get_db()
    user = await db.users.find_one({"username": body.username})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": body.username, "language": user["language"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"username": user["username"], "language": user["language"]},
    }


@router.put("/language")
async def update_language(body: LanguageUpdate, user: dict = Depends(get_current_user)):
    db = get_db()
    await db.users.update_one(
        {"username": user["sub"]},
        {"$set": {"language": body.language}}
    )
    return {"message": "Language updated"}
