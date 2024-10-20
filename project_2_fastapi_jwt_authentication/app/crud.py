from sqlmodel import Session
from . import models_and_schemas
from . import auth

def create_user(db: Session, user: models_and_schemas.UserSchema) -> models_and_schemas.User:
    """Create a new User"""
    hashed_password = auth.create_password_hash(user.password)
    db_user = models_and_schemas.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    """Get all Users"""
    users = db.query(models_and_schemas.User).all()
    return users

def get_user_by_username(db: Session, username: str) -> models_and_schemas.User:
    """Get a User by username"""
    user = db.query(models_and_schemas.User).filter(models_and_schemas.User.username == username).first()
    return user
