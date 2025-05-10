from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import database
from app.models import areas
from app.schemas import AreaCreate, AreaRead, AreaUpdate

router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
)

@router.post("/", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
async def create_area(area: AreaCreate):
    query = areas.insert().values(**area.dict())
    area_id = await database.execute(query)
    return {**area.dict(), "id": area_id}

@router.get("/", response_model=List[AreaRead])
async def read_areas():
    query = areas.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=AreaRead)
async def read_area(id: int):
    query = areas.select().where(areas.c.id == id)
    area = await database.fetch_one(query)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area nicht gefunden",
        )
    return area

@router.put("/{id}", response_model=AreaRead)
async def update_area(id: int, area: AreaUpdate):
    # Nur die Felder aktualisieren, die nicht None sind
    values = {k: v for k, v in area.dict().items() if v is not None}
    query = (
        areas.update()
        .where(areas.c.id == id)
        .values(**values)
        .returning(areas)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area nicht gefunden",
        )
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_area(id: int):
    query = areas.delete().where(areas.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area nicht gefunden",
        )
    # FastAPI kümmert sich um den 204-Response
    return None
