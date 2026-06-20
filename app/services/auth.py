from sqlalchemy.orm import Session
from app.schemas.user import LoginRequest, RegisterRequest
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException


def register_user(db: Session, user_data: RegisterRequest):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

def login_user(db: Session, user_data: LoginRequest):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
