from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserOut, Token, UserLogin,UserLoginResponse
from crud import user_crud
from auth.auth_handler import create_access_token, verify_password
from models import User

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
def login(form: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token(data={"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "full_name": user.full_name,
        "email": user.email,
    }
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_crud.create_user(db, user)

@router.get("/exists")
def user_exists(db: Session = Depends(get_db)):
    exists = db.query(User).count() > 0
    return {"exists": exists}