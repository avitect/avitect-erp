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

positions = Table(
    "positions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=False),
    Column("name", String, nullable=False),
)

systems = Table(
    "systems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=False),
    Column("name", String, nullable=False),
)

devices = Table(
    "devices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("system_id", Integer, ForeignKey("systems.id"), nullable=False),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=True),
    Column("area_id", Integer, ForeignKey("areas.id"), nullable=True),
    Column("roomgroup_id", Integer, ForeignKey("roomgroups.id"), nullable=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=True),
    Column("position_id", Integer, ForeignKey("positions.id"), nullable=True),
    Column("name", String, nullable=False),
    Column("device_type", String, nullable=False),
)

ports = Table(
    "ports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("direction", String, nullable=False),      # input/output
    Column("connectivity", String, nullable=False),   # wired/wireless
    Column("connector_type", String, nullable=True),  # Stecker-Typ
    Column("signal_type", String, nullable=True),     # Signal-Art
)

connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("from_device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("from_port_id",   Integer, ForeignKey("ports.id"),   nullable=False),
    Column("to_device_id",   Integer, ForeignKey("devices.id"), nullable=False),
    Column("to_port_id",     Integer, ForeignKey("ports.id"),   nullable=False),
    Column("cable_type",     String,  nullable=True),
    Column("cable_length",   Float,   nullable=True),
)
