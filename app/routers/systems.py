from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import systems
from app.schemas import SystemCreate, SystemRead
from app.auth import get_current_user

router = APIRouter(prefix="/systems", tags=["systems"])

@router.post("/", response_model=SystemRead, status_code=status.HTTP_201_CREATED)
async def create_system(data: SystemCreate, user=Depends(get_current_user)):
    sys_id = await database.execute(systems.insert().values(**data.dict()))
    return {**data.dict(), "id": sys_id}

@router.get("/", response_model=List[SystemRead])
async def list_systems(user=Depends(get_current_user)):
    return await database.fetch_all(systems.select())

@router.get("/{sys_id}", response_model=SystemRead)
async def get_system(sys_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(systems.select().where(systems.c.id==sys_id))
    if not row:
        raise HTTPException(status_code=404, detail="System not found")
    return row

@router.delete("/{sys_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(sys_id: int, user=Depends(get_current_user)):
    await database.execute(systems.delete().where(systems.c.id==sys_id))
    return
