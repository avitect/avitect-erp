from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import objects
from app.schemas import ObjectCreate, ObjectRead
from app.auth import get_current_user

router = APIRouter(prefix="/objects", tags=["objects"])

@router.post("/", response_model=ObjectRead, status_code=status.HTTP_201_CREATED)
async def create_object(data: ObjectCreate, user=Depends(get_current_user)):
    obj_id = await database.execute(objects.insert().values(**data.dict()))
    return {**data.dict(), "id": obj_id}

@router.get("/", response_model=List[ObjectRead])
async def list_objects(user=Depends(get_current_user)):
    return await database.fetch_all(objects.select())

@router.get("/{object_id}", response_model=ObjectRead)
async def get_object(object_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(objects.select().where(objects.c.id == object_id))
    if not row:
        raise HTTPException(status_code=404, detail="Object not found")
    return row

@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_object(object_id: int, user=Depends(get_current_user)):
    await database.execute(objects.delete().where(objects.c.id == object_id))
    return
