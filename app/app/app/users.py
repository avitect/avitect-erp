from fastapi_users import FastAPIUsers, models as fa_models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from app.database import database
from app.models import users as users_table

SECRET = "DEIN-SEHR-SICHERES-SECRET"

class User(fa_models.BaseUser):
    role: str

class UserCreate(fa_models.BaseUserCreate):
    role: str

class UserUpdate(fa_models.BaseUserUpdate):
    role: str

class UserDB(User, fa_models.BaseUserDB):
    pass

user_db = SQLAlchemyUserDatabase(UserDB, database, users_table)
jwt_auth = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_auth],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

get_current_active_user = fastapi_users.current_user(active=True)
