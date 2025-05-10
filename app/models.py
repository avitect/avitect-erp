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
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.database import metadata

# ... Dein users-Table oben bleibt bestehen ...

customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=True),
    Column("phone", String, nullable=True),
)

from sqlalchemy import ForeignKey

objects = Table(
    "objects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
)

from sqlalchemy import ForeignKey

areas = Table(
    "areas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=False),
    Column("name", String, nullable=False),
)

roomgroups = Table(
    "roomgroups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("area_id", Integer, ForeignKey("areas.id"), nullable=False),
    Column("name", String, nullable=False),
)


rooms = Table(
    "rooms",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("area_id", Integer, ForeignKey("areas.id"), nullable=False),
    Column("name", String, nullable=False),
)
