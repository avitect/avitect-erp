from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import database
from app.models import systems, objects
from app.schemas import SystemCreate, SystemRead, SystemUpdate
from app.auth import get_current_user

router = APIRouter(
    prefix="/systems",
    tags=["Systems"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=SystemRead, status_code=status.HTTP_201_CREATED)
async def create_system(system: SystemCreate):
    # prüfen, ob das Objekt existiert
    obj_query = objects.select().where(objects.c.id == system.object_id)
    if not await database.fetch_one(obj_query):
        raise HTTPException(status_code=404, detail="Object nicht gefunden")

    query = systems.insert().values(**system.dict())
    system_id = await database.execute(query)
    return {**system.dict(), "id": system_id}

@router.get("/", response_model=List[SystemRead])
async def read_systems():
    query = systems.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=SystemRead)
async def read_system(id: int):
    query = systems.select().where(systems.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="System nicht gefunden")
    return result

@router.put("/{id}", response_model=SystemRead)
async def update_system(id: int, system: SystemUpdate):
    # bei Änderung von object_id prüfen wir die Existenz
    if system.object_id is not None:
        obj_query = objects.select().where(objects.c.id == system.object_id)
        if not await database.fetch_one(obj_query):
            raise HTTPException(status_code=404, detail="Object nicht gefunden")

    values = {k: v for k, v in system.dict().items() if v is not None}
    query = (
        systems.update()
        .where(systems.c.id == id)
        .values(**values)
        .returning(systems)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(status_code=404, detail="System nicht gefunden")
    return updated
