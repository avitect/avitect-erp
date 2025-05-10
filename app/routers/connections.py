from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import connections
from app.schemas import ConnectionCreate, ConnectionRead
from app.auth import get_current_user

router = APIRouter(prefix="/connections", tags=["connections"])

@router.post("/", response_model=ConnectionRead, status_code=status.HTTP_201_CREATED)
async def create_connection(data: ConnectionCreate, user=Depends(get_current_user)):
    # 1. Hol die beiden Port-Datensätze
    from_port = await database.fetch_one(ports.select().where(ports.c.id == data.from_port_id))
    to_port   = await database.fetch_one(ports.select().where(ports.c.id == data.to_port_id))

    # 2. Existenz prüfen
    if not from_port or not to_port:
        raise HTTPException(status_code=404, detail="Port nicht gefunden")

    # 3. Richtung prüfen: Ausgang → Eingang
    if from_port["direction"] != "output" or to_port["direction"] != "input":
        raise HTTPException(
            status_code=400,
            detail="Verbindung muss von einem Output-Port zu einem Input-Port führen"
        )

    # 4. Signal-Typen abgleichen
    if from_port["signal_type"] != to_port["signal_type"]:
        raise HTTPException(
            status_code=400,
            detail=f"Signal-Typen stimmen nicht überein: {from_port['signal_type']} ≠ {to_port['signal_type']}"
        )

    # 5. (Optional) Wired/Wireless-Mix prüfen
    if from_port["connectivity"] != to_port["connectivity"]:
        raise HTTPException(
            status_code=400,
            detail="Kabelverbindung muss wired–wired oder wireless–wireless sein"
        )

    # 6. Wenn alles passt, Connection anlegen
    cid = await database.execute(connections.insert().values(**data.dict()))
    return {**data.dict(), "id": cid}


@router.get("/", response_model=List[ConnectionRead])
async def list_connections(user=Depends(get_current_user)):
    return await database.fetch_all(connections.select())

@router.get("/{cid}", response_model=ConnectionRead)
async def get_connection(cid: int, user=Depends(get_current_user)):
    row = await database.fetch_one(connections.select().where(connections.c.id==cid))
    if not row:
        raise HTTPException(404, "Connection not found")
    return row

@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(cid: int, user=Depends(get_current_user)):
    await database.execute(connections.delete().where(connections.c.id==cid))
    return
