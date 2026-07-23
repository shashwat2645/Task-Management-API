from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema, LoginSchema
from src.user.models import UserModel
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError 
from src.utils.settings import settings
from datetime import UTC, datetime, timedelta
from src.utils.mail import send_mail

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

async def register(body: UserSchema, db: Session, bg_task: BackgroundTasks):
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

  
    # pyrefly: ignore [bad-argument-type]
    bg_task.add_task(send_mail, [new_user.email])

    return new_user


def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    # pyrefly: ignore [bad-argument-type]
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    exp_time = datetime.now(UTC) + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id":user.id, "exp": exp_time}, settings.SECRET_KEY, settings.ALGORITHM)

    return {"token": token}


def is_authenticated(request: Request, db: Session):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
        token = token.split(" ")[-1] 

        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")