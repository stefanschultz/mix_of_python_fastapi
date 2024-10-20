from sqlmodel import Session
from . import models_and_schemas

def create_user(db: Session, user: models_and_schemas.UserSchema) -> models_and_schemas.User:
    """Create a new User"""
    hashed_password = user.password + "notreallyhashed"
    db_user = models_and_schemas.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=False,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
