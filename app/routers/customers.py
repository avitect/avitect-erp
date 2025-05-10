from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.database import database
from app.models import devices
from app.schemas import DeviceCreate, DeviceRead, DeviceUpdate

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)

@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate):
    query = devices.insert().values(**device.dict())
    device_id = await database.execute(query)
    return {**device.dict(), "id": device_id}

@router.get("/", response_model=List[DeviceRead])
async def read_devices():
    query = devices.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=DeviceRead)
async def read_device(id: int):
    query = devices.select().where(devices.c.id == id)
    device = await database.fetch_one(query)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device nicht gefunden",
        )
    return device

@router.put("/{id}", response_model=DeviceRead)
async def update_device(id: int, device: DeviceUpdate):
    values = {k: v for k, v in device.dict().items() if v is not None}
    query = (
        devices.update()
        .where(devices.c.id == id)
        .values(**values)
        .returning(devices)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device nicht gefunden",
        )
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(id: int):
    query = devices.delete().where(devices.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device nicht gefunden",
        )
    return None
