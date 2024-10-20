from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from dotenv import find_dotenv, load_dotenv
from . import database
from . import models_and_schemas
from . import crud
from . import auth
from . import sendmail

load_dotenv(find_dotenv())

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Create the database and tables"""
    database.create_db_and_tables()

@app.on_event("shutdown")
def shutdown_event():
    """"""
    database.shutdown_db()

@app.post("/register")
def register_user(user: models_and_schemas.UserSchema, db: Session = Depends(database.get_db)) -> models_and_schemas.User:
    """Register a new user"""
    db_user = crud.create_user(db, user)
    token = auth.create_access_token(db_user)
    # Uncomment the line below to send an email to the user
    # sendmail.send_email(to=db_user.email, token=token, username=db_user.username)
    return db_user

@app.post("/login")
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user"""
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")
    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {"access_token": token, "token_type": "Bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

@app.get("/verify/{token}", response_class=HTMLResponse)
def verify_user(token: str, db: Session = Depends(database.get_db)):
    """Verify a user"""
    claims = auth.decode_token(token)
    username = claims.get("sub")
    db_user = crud.get_user_by_username(db=db, username=username)
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return f"""
    <html>
    <head>
        <title>User Verification</title>
    </head>
    <body>
        <h1>User Verification</h1>
        <p>User {username} has been verified.</p>
    </body>
    </html>
    """


@app.get("/users")
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    """Get all users"""
    users = crud.get_users(db=db)
    return users

@app.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    """Secured: Get all users"""
    users = crud.get_users(db=db)
    return users

@app.get("/adminsonly", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(database.get_db)) -> list[models_and_schemas.User]:
    """Admins Only: Get all users"""
    users = crud.get_users(db=db)
    return users