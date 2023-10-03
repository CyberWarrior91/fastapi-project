from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, TIMESTAMP
from src.database import Base


class Operation(Base):
    __tablename__ = "operation"

    id = mapped_column(Integer, primary_key=True)
    quantity = mapped_column(String)
    figi = mapped_column(String)
    instrument_type = mapped_column(String, nullable=True)
    date = mapped_column(TIMESTAMP)
    type = mapped_column(String)
