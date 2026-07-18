from sqlalchemy.orm import Session
from src.user.dtos import UserSchema, LoginSchema
from src.user.models import UserModel
from fastapi import HTTPException, status
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import UTC, datetime, timedelta

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def register(body: UserSchema, db: Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exists")
    
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="Email already exists")
    
    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        password_hash=hash_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    exp_time = datetime.now(UTC) + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id":user.id, "exp": exp_time}, settings.SECRET_KEY, settings.ALGORITHM)

    return {"token": token}