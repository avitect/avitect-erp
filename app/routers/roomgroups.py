from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import roomgroups
from app.schemas import RoomGroupCreate, RoomGroupRead
from app.auth import get_current_user

router = APIRouter(prefix="/roomgroups", tags=["roomgroups"])

@router.post("/", response_model=RoomGroupRead, status_code=status.HTTP_201_CREATED)
async def create_roomgroup(data: RoomGroupCreate, user=Depends(get_current_user)):
    rg_id = await database.execute(roomgroups.insert().values(**data.dict()))
    return {**data.dict(), "id": rg_id}

@router.get("/", response_model=List[RoomGroupRead])
async def list_roomgroups(user=Depends(get_current_user)):
    return await database.fetch_all(roomgroups.select())

@router.get("/{rg_id}", response_model=RoomGroupRead)
async def get_roomgroup(rg_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(roomgroups.select().where(roomgroups.c.id==rg_id))
    if not row:
        raise HTTPException(status_code=404, detail="RoomGroup not found")
    return row

@router.delete("/{rg_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roomgroup(rg_id: int, user=Depends(get_current_user)):
    await database.execute(roomgroups.delete().where(roomgroups.c.id==rg_id))
    return
