from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import database
from app.models import positions, rooms
from app.schemas import PositionCreate, PositionRead, PositionUpdate
from app.auth import get_current_user

router = APIRouter(
    prefix="/positions",
    tags=["Positions"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(position: PositionCreate):
    # sicherstellen, dass der Raum existiert
    room_query = rooms.select().where(rooms.c.id == position.room_id)
    if not await database.fetch_one(room_query):
        raise HTTPException(status_code=404, detail="Room nicht gefunden")

    query = positions.insert().values(**position.dict())
    pos_id = await database.execute(query)
    return {**position.dict(), "id": pos_id}

@router.get("/", response_model=List[PositionRead])
async def read_positions():
    query = positions.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=PositionRead)
async def read_position(id: int):
    query = positions.select().where(positions.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Position nicht gefunden")
    return result

@router.put("/{id}", response_model=PositionRead)
async def update_position(id: int, position: PositionUpdate):
    # falls room_id geändert wird, prüfen wir die Existenz
    if position.room_id is not None:
        room_query = rooms.select().where(rooms.c.id == position.room_id)
        if not await database.fetch_one(room_query):
            raise HTTPException(status_code=404, detail="Room nicht gefunden")

    values = {k: v for k, v in position.dict().items() if v is not None}
    query = (
        positions.update()
        .where(positions.c.id == id)
        .values(**values)
        .returning(positions)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(status_code=404, detail="Position nicht gefunden")
    return updated
