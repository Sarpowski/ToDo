from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, SessionLocal
from .schemas import UserCreate, UserOut
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- API ROUTES FIRST ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(
        db,
        user.username,
        user.email,
        user.password
    )

@app.get("/api/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# ---------------- STATIC FILES LAST ----------------

app.mount(
    "/",
    StaticFiles(directory="client", html=True),
    name="client",
)