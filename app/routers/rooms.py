from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import database
from app.models import rooms, areas
from app.schemas import RoomCreate, RoomRead, RoomUpdate
from app.auth import get_current_user

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomCreate):
    # prüfen, ob der Bereich existiert
    area_query = areas.select().where(areas.c.id == room.area_id)
    if not await database.fetch_one(area_query):
        raise HTTPException(status_code=404, detail="Area nicht gefunden")

    query = rooms.insert().values(**room.dict())
    room_id = await database.execute(query)
    return {**room.dict(), "id": room_id}

@router.get("/", response_model=List[RoomRead])
async def read_rooms():
    query = rooms.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=RoomRead)
async def read_room(id: int):
    query = rooms.select().where(rooms.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Room nicht gefunden")
    return result

@router.put("/{id}", response_model=RoomRead)
async def update_room(id: int, room: RoomUpdate):
    # bei Änderung von area_id prüfen wir die Existenz
    if room.area_id is not None:
        area_query = areas.select().where(areas.c.id == room.area_id)
        if not await database.fetch_one(area_query):
            raise HTTPException(status_code=404, detail="Area nicht gefunden")

    values = {k: v for k, v in room.dict().items() if v is not None}
    query = (
        rooms.update()
        .where(rooms.c.id == id)
        .values(**values)
        .returning(rooms)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(status_code=404, detail="Room nicht gefunden")
    return updated
