from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from . import database
from . import models_and_schemas
from . import crud
from . import auth

app = FastAPI()

@app.on_event("startup")
def startup_event():
    database.create_db_and_tables()

@app.on_event("shutdown")
def shutdown_event():
    database.shutdown_db()

@app.post("/register")
def register_user(user: models_and_schemas.UserSchema, db: Session = Depends(database.get_db)) -> models_and_schemas.User:
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login")
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a User"""
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")
    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {"access_token": token, "token_type": "Bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

@app.get("/users")
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    users = crud.get_users(db=db)
    return users

@app.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    users = crud.get_users(db=db)
    return users

@app.get("/adminsonly", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    users = crud.get_users(db=db)
    return users