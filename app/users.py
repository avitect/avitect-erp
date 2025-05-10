from fastapi_users import FastAPIUsers, models as fa_models
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from app.database import database
from app.models import users as users_table

SECRET = "DEIN-SEHR-SICHERES-SECRET"

# FastAPI-Users-Modelle
class User(fa_models.BaseUser):
    role: str

class UserCreate(fa_models.BaseUserCreate):
    role: str

class UserUpdate(fa_models.BaseUserUpdate):
    role: str

class UserDB(User, fa_models.BaseUserDB):
    pass

# Datenbank-Adapter
user_db = SQLAlchemyUserDatabase(UserDB, database, users_table)

# Auth-Backend mit JWT-Cookie
cookie_transport = CookieTransport(cookie_name="avitect_auth", cookie_max_age=3600)
jwt_strategy = JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=lambda: jwt_strategy,
)

# FastAPIUsers-Instanz
fastapi_users = FastAPIUsers(
    user_db,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

get_current_active_user = fastapi_users.current_user(active=True)
