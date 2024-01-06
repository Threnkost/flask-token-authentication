from sqlalchemy import (
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class User(Base):
    __tablename__ = "user_accounts"
    
    id: Mapped[int]       = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"