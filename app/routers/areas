from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import areas
from app.schemas import AreaCreate, AreaRead
from app.auth import get_current_user

router = APIRouter(prefix="/areas", tags=["areas"])

@router.post("/", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
async def create_area(data: AreaCreate, user=Depends(get_current_user)):
    area_id = await database.execute(areas.insert().values(**data.dict()))
    return {**data.dict(), "id": area_id}

@router.get("/", response_model=List[AreaRead])
async def list_areas(user=Depends(get_current_user)):
    return await database.fetch_all(areas.select())

@router.get("/{area_id}", response_model=AreaRead)
async def get_area(area_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(areas.select().where(areas.c.id==area_id))
    if not row:
        raise HTTPException(status_code=404, detail="Area not found")
    return row

@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_area(area_id: int, user=Depends(get_current_user)):
    await database.execute(areas.delete().where(areas.c.id==area_id))
    return
