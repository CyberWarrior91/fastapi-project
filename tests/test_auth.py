import pytest
from sqlalchemy import insert, select

from src.auth.models import Role
from tests.conftest import client, async_session_maker

async def test_add_role():
    async with async_session_maker() as session:
        role_table = Role.__table__
        stmt = insert(role_table).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role_table)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Role was not added"


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })
    assert response.status_code == 201
