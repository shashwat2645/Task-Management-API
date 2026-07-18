from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False) 
    # created_at = Column(DateTime)
    # updated_at = Column(DateTime)
    # is_active = Column(Boolean)