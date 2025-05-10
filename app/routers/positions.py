from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import positions
from app.schemas import PositionCreate, PositionRead
from app.auth import get_current_user

router = APIRouter(prefix="/positions", tags=["positions"])

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(data: PositionCreate, user=Depends(get_current_user)):
    pos_id = await database.execute(positions.insert().values(**data.dict()))
    return {**data.dict(), "id": pos_id}

@router.get("/", response_model=List[PositionRead])
async def list_positions(user=Depends(get_current_user)):
    return await database.fetch_all(positions.select())

@router.get("/{pos_id}", response_model=PositionRead)
async def get_position(pos_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(positions.select().where(positions.c.id==pos_id))
    if not row:
        raise HTTPException(status_code=404, detail="Position not found")
    return row

@router.delete("/{pos_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(pos_id: int, user=Depends(get_current_user)):
    await database.execute(positions.delete().where(positions.c.id==pos_id))
    return
