from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import database
from app.models import connections
from app.schemas import ConnectionCreate, ConnectionRead, ConnectionUpdate

router = APIRouter(
    prefix="/connections",
    tags=["Connections"],
)

@router.post("/", response_model=ConnectionRead, status_code=status.HTTP_201_CREATED)
async def create_connection(conn: ConnectionCreate):
    query = connections.insert().values(**conn.dict())
    conn_id = await database.execute(query)
    return {**conn.dict(), "id": conn_id}

@router.get("/", response_model=List[ConnectionRead])
async def read_connections():
    query = connections.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=ConnectionRead)
async def read_connection(id: int):
    query = connections.select().where(connections.c.id == id)
    connection = await database.fetch_one(query)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection nicht gefunden",
        )
    return connection

@router.put("/{id}", response_model=ConnectionRead)
async def update_connection(id: int, conn: ConnectionUpdate):
    values = {k: v for k, v in conn.dict().items() if v is not None}
    query = (
        connections.update()
        .where(connections.c.id == id)
        .values(**values)
        .returning(connections)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection nicht gefunden",
        )
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(id: int):
    query = connections.delete().where(connections.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection nicht gefunden",
        )
    return None
