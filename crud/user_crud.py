from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth.auth_handler import hash_password

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = User(**user.dict(exclude={"password"}), password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user