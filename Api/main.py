from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔥 API ROUTES FIRST
@app.post("/api/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.username, user.email, user.password)

@app.get("/api/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# 🔥 STATIC FILES LAST (VERY IMPORTANT)
app.mount(
    "/",
    StaticFiles(directory="client", html=True),
    name="client",
)