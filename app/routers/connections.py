from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import connections
from app.schemas import ConnectionCreate, ConnectionRead
from app.auth import get_current_user

router = APIRouter(prefix="/connections", tags=["connections"])

@router.post("/", response_model=ConnectionRead, status_code=status.HTTP_201_CREATED)
async def create_connection(data: ConnectionCreate, user=Depends(get_current_user)):
    cid = await database.execute(connections.insert().values(**data.dict()))
    return {**data.dict(), "id": cid}

@router.get("/", response_model=List[ConnectionRead])
async def list_connections(user=Depends(get_current_user)):
    return await database.fetch_all(connections.select())

@router.get("/{cid}", response_model=ConnectionRead)
async def get_connection(cid: int, user=Depends(get_current_user)):
    row = await database.fetch_one(connections.select().where(connections.c.id==cid))
    if not row:
        raise HTTPException(404, "Connection not found")
    return row

@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(cid: int, user=Depends(get_current_user)):
    await database.execute(connections.delete().where(connections.c.id==cid))
    return
