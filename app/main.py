from fastapi import FastAPI, Depends
from app.database import database, engine, metadata
from app.auth import router as auth_router, get_current_user
from app.models import users as users_table
from app.routers.customers import router as customers_router
from app.routers.objects   import router as objects_router
from app.routers.areas import router as areas_router
from app.routers.rooms import router as rooms_router



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
app.include_router(rooms_router)


# Geschützter Beispiel-Endpoint
@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"email": user["email"], "role": user["role"]}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
