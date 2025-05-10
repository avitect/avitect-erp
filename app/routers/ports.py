from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import ports
from app.schemas import PortCreate, PortRead
from app.auth import get_current_user

router = APIRouter(prefix="/ports", tags=["ports"])

@router.post("/", response_model=PortRead, status_code=status.HTTP_201_CREATED)
async def create_port(data: PortCreate, user=Depends(get_current_user)):
    pid = await database.execute(ports.insert().values(**data.dict()))
    return {**data.dict(), "id": pid}

@router.get("/", response_model=List[PortRead])
async def list_ports(user=Depends(get_current_user)):
    return await database.fetch_all(ports.select())

@router.get("/{pid}", response_model=PortRead)
async def get_port(pid: int, user=Depends(get_current_user)):
    row = await database.fetch_one(ports.select().where(ports.c.id==pid))
    if not row:
        raise HTTPException(404, "Port not found")
    return row

@router.delete("/{pid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_port(pid: int, user=Depends(get_current_user)):
    await database.execute(ports.delete().where(ports.c.id==pid))
    return
