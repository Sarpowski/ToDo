from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .models import User
def create_user(db: Session, username: str, email: str, password: str):
    user = User(
        username=username,
        email=email,
        hashed_password=bcrypt.hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()