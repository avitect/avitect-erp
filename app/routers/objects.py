from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import database
from app.models import objects
from app.schemas import ObjectCreate, ObjectRead, ObjectUpdate

router = APIRouter(
    prefix="/objects",
    tags=["Objects"],
)

@router.post("/", response_model=ObjectRead, status_code=status.HTTP_201_CREATED)
async def create_object(obj: ObjectCreate):
    query = objects.insert().values(**obj.dict())
    obj_id = await database.execute(query)
    return {**obj.dict(), "id": obj_id}

@router.get("/", response_model=List[ObjectRead])
async def read_objects():
    query = objects.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=ObjectRead)
async def read_object(id: int):
    query = objects.select().where(objects.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object nicht gefunden",
        )
    return result

@router.put("/{id}", response_model=ObjectRead)
async def update_object(id: int, obj: ObjectUpdate):
    values = {k: v for k, v in obj.dict().items() if v is not None}
    query = (
        objects.update()
        .where(objects.c.id == id)
        .values(**values)
        .returning(objects)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object nicht gefunden",
        )
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_object(id: int):
    query = objects.delete().where(objects.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object nicht gefunden",
        )
    return None
