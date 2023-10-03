from datetime import datetime
from sqlalchemy import JSON, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from src.database import Base


# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    registered_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id = mapped_column(ForeignKey('role.id'))
    role = relationship('Role', backref='users')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class Role(Base):
    __tablename__ = "role"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    permissions = mapped_column(JSON)
