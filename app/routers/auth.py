from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model= RegisterResponse)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login", response_model=LoginResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, user)