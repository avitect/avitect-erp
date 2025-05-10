from fastapi import FastAPI, Depends
from app.database import database, engine, metadata
from app.auth import router as auth_router, get_current_user
from app.models import users as users_table

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

# Geschützter Beispiel-Endpoint
@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"email": user["email"], "role": user["role"]}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
