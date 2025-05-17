# app/routers/devices.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DeviceCreate, Device
from app.models import devices as devices_table, Device as DeviceModel

router = APIRouter()

@router.post("/devices/", response_model=Device)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    # Nur gültige Felder übergeben (None und roomgroup_id rausfiltern)
    data = device.dict(exclude_none=True, exclude={"roomgroup_id"})
    try:
        result = db.execute(devices_table.insert().values(**data))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Datenbank-Fehler: {e}")
    new_id = result.inserted_primary_key[0]
    new_device = db.query(DeviceModel).get(new_id)
    if not new_device:
        raise HTTPException(status_code=404, detail="Device wurde nicht gefunden")
    return new_device
