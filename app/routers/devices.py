from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import devices
from app.schemas import DeviceCreate, DeviceRead
from app.auth import get_current_user

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device(data: DeviceCreate, user=Depends(get_current_user)):
    dev_id = await database.execute(devices.insert().values(**data.dict()))
    return {**data.dict(), "id": dev_id}

@router.get("/", response_model=List[DeviceRead])
async def list_devices(user=Depends(get_current_user)):
    return await database.fetch_all(devices.select())

@router.get("/{dev_id}", response_model=DeviceRead)
async def get_device(dev_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(devices.select().where(devices.c.id==dev_id))
    if not row:
        raise HTTPException(status_code=404, detail="Device not found")
    return row

@router.delete("/{dev_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(dev_id: int, user=Depends(get_current_user)):
    await database.execute(devices.delete().where(devices.c.id==dev_id))
    return
