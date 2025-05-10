from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import database
from app.models import ports, devices
from app.schemas import PortCreate, PortRead, PortUpdate
from app.auth import get_current_user

router = APIRouter(
    prefix="/ports",
    tags=["Ports"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PortRead, status_code=status.HTTP_201_CREATED)
async def create_port(port: PortCreate):
    # sicherstellen, dass das Gerät existiert
    device_query = devices.select().where(devices.c.id == port.device_id)
    if not await database.fetch_one(device_query):
        raise HTTPException(status_code=404, detail="Device nicht gefunden")

    query = ports.insert().values(**port.dict())
    port_id = await database.execute(query)
    return {**port.dict(), "id": port_id}

@router.get("/", response_model=List[PortRead])
async def read_ports():
    query = ports.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=PortRead)
async def read_port(id: int):
    query = ports.select().where(ports.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Port nicht gefunden")
    return result

@router.put("/{id}", response_model=PortRead)
async def update_port(id: int, port: PortUpdate):
    # falls device_id geändert wird, prüfen wir die Existenz
    if port.device_id is not None:
        device_query = devices.select().where(devices.c.id == port.device_id)
        if not await database.fetch_one(device_query):
            raise HTTPException(status_code=404, detail="Device nicht gefunden")

    values = {k: v for k, v in port.dict().items() if v is not None}
    query = (
        ports.update()
        .where(ports.c.id == id)
        .values(**values)
        .returning(ports)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(status_code=404, detail="Port nicht gefunden")
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_port(id: int):
    query = ports.delete().where(ports.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Port nicht gefunden")
    return None
