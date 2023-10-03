import time
from fastapi import APIRouter, HTTPException
from src.operations.schemas import OperationCreate
from sqlalchemy import insert, select
from src.operations.models import Operation
from src.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    operation_table = Operation.__table__
    try:
        query = select(operation_table).where(operation_table.c.type.like(f"%{operation_type}%"))
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    operation_table = Operation.__table__
    stmt = insert(operation_table).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
