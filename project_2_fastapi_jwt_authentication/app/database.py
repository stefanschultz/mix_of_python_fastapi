from sqlmodel import Session, SQLModel, create_engine
from pathlib import Path
import os

# Define the database URL
SQLITE_DATABASE_URL = "sqlite:///sql_app.db"

# Create a database connection
engine = create_engine(url=SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})

def get_db():
    """Get a database connection"""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create the database and tables"""
    SQLModel.metadata.create_all(engine)

def shutdown_db():
    """Remove the database file"""
    cwd = Path.cwd().resolve()
    db_file = [file for file in os.listdir() if file.endswith(".db")][0]
    os.remove(os.path.join(cwd, db_file))
