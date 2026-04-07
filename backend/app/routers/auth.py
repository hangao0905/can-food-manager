import hashlib
import jwt
import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.models import User

router = APIRouter(prefix="/auth", tags=["认证"])

JWT_SECRET = "can-food-manager-secret-key-2024"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24 * 7

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

def hash_password(password: str) -> str:
    salt = "can_food_salt_v1"
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return key.hex()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_token(user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRE_HOURS),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效Token")

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> dict:
    """获取当前登录用户（FastAPI 依赖）"""
    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization
    payload = decode_token(token)
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="用户已被停用")
    return {"id": user.id, "username": user.username, "role": user.role}

def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """仅允许管理员"""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="用户已被停用，请联系管理员")
    token = create_token(user.id, user.username)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user={"id": user.id, "username": user.username, "role": user.role}
    )

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
