from pydantic_core.core_schema import nullable_schema
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # created_at = Column(DateTime)
    # updated_at = Column(DateTime)
    # is_active = Column(Boolean)