from fastapi import FastAPI, Depends
from app.database import database, engine, metadata
from app.users import fastapi_users, jwt_auth, get_current_active_user
from app.models import users as users_table

app = FastAPI()

# Tabellen anlegen
metadata.create_all(bind=engine)

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

# Auth-Router
app.include_router(
    fastapi_users.get_auth_router(jwt_auth), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(), prefix="/users", tags=["users"]
)

# Geschützter Test-Endpoint
@app.get("/protected")
async def protected_route(user=Depends(get_current_active_user)):
    return {"email": user.email, "role": user.role}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
