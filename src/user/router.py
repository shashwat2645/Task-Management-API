from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.user.dtos import LoginSchema, UserSchema, ResponseSchema
from src.utils.db import get_db
from src.user import controller

user_routes = APIRouter(prefix='/user')

@user_routes.post('/register', response_model=ResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    print(body)
    return controller.register(body, db)


@user_routes.post('/login', status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)