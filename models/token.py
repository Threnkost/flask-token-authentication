from sqlalchemy import (
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from .base import Base


class Token(Base):
    __tablename__ = "tokens"
    
    id: Mapped[int]         = mapped_column(primary_key=True)
    user: Mapped[int]       = mapped_column(ForeignKey("user_accounts.id"))
    token: Mapped[str]      = mapped_column(String)
    created_at: Mapped[float] = mapped_column(Float)
    expires_at: Mapped[float] = mapped_column(Float)