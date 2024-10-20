from http.client import HTTPException
from passlib.context import CryptContext
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import models_and_schemas

JWT_SECRET = "secret"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_password_hash(password: str) -> str:
    """Create a password hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models_and_schemas.User) -> str:
    """Create an access token"""
    claims = {
        "sub": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=120)
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    """Decode a token"""
    claims = jwt.decode(token, key=JWT_SECRET, algorithms=["HS256"])
    return claims

def check_active(token: str = Depends(oauth2_scheme)) -> dict:
    """Check if a token is active"""
    claims = decode_token(token)
    if claims.get("active"):
        return claims
    raise HTTPException(
        status_code=401,
        detail="Please activate your account",
        headers={"WWW-Authenticate": "Bearer"}
    )

def check_admin(claims: dict = Depends(check_active)) -> dict:
    role = claims.get("role")
    if not role == "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource. You must be an admin.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return claims