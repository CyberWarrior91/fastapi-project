from datetime import datetime
from sqlalchemy import JSON, MetaData, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    pass


# an example mapping using the base
class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    password = mapped_column(String, nullable=False)
    registered_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id = mapped_column(ForeignKey("roles.id"))


class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    permissions = mapped_column(JSON)
