from sqlalchemy import Table, Column, Integer, String
from app.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role", String, nullable=False, default="integrator"),
)
