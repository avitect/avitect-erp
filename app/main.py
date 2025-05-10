from fastapi import FastAPI, Depends
from sqlalchemy import Float
from app.database import database, engine, metadata
from app.auth import router as auth_router, get_current_user
from app.models import users as users_table
from app.routers.customers import router as customers_router
from app.routers.objects   import router as objects_router
from app.routers.areas import router as areas_router
from app.routers.roomgroups import router as roomgroups_router
from app.routers.rooms import router as rooms_router
from app.routers.positions import router as positions_router
from app.routers.systems import router as systems_router
from app.routers.devices import router as devices_router
from app.routers.ports       import router as ports_router
from app.routers.connections import router as connections_router


# Tabellen anlegen
metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

# Auth-Router
app.include_router(auth_router)
from app.routers.customers import router as customers_router

app.include_router(customers_router)
app.include_router(objects_router)
app.include_router(areas_router)
app.include_router(roomgroups_router)
app.include_router(rooms_router)
app.include_router(positions_router)
app.include_router(systems_router)
app.include_router(devices_router)
app.include_router(ports_router)
app.include_router(connections_router)


# Geschützter Beispiel-Endpoint
@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"email": user["email"], "role": user["role"]}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
