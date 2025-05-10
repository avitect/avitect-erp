from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import rooms
from app.schemas import RoomCreate, RoomRead
from app.auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(data: RoomCreate, user=Depends(get_current_user)):
    room_id = await database.execute(rooms.insert().values(**data.dict()))
    return {**data.dict(), "id": room_id}

@router.get("/", response_model=List[RoomRead])
async def list_rooms(user=Depends(get_current_user)):
    return await database.fetch_all(rooms.select())

@router.get("/{room_id}", response_model=RoomRead)
async def get_room(room_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(rooms.select().where(rooms.c.id==room_id))
    if not row:
        raise HTTPException(status_code=404, detail="Room not found")
    return row

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, user=Depends(get_current_user)):
    await database.execute(rooms.delete().where(rooms.c.id==room_id))
    return
