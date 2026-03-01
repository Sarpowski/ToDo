import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .schemas import UserCreate, UserOut
from . import crud

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_DIR = os.path.join(BASE_DIR, "client")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API FIRST
@app.post("/api/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.username, user.email, user.password)

@app.get("/api/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# STATIC LAST (ABSOLUTE PATH)
app.mount(
    "/",
    StaticFiles(directory=CLIENT_DIR, html=True),
    name="client",
)