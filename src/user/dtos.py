from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

class ResponseSchema(BaseModel):
    name: str
    username: str
    email: str
    id: int

class LoginSchema(BaseModel):
    username: str
    password: str
    