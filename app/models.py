from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from app.database import metadata

# Users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role", String, nullable=False, default="integrator"),
)

# Customers table
customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=True),
    Column("phone", String, nullable=True),
)

# Objects (Immobilien)
objects = Table(
    "objects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
)

# Areas (Bereiche)
areas = Table(
    "areas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=False),
    Column("name", String, nullable=False),
)

# Room Groups (Raumgruppen)
room_groups = Table(
    "room_groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("area_id", Integer, ForeignKey("areas.id"), nullable=False),
    Column("name", String, nullable=False),
)

# Rooms (Räume)
rooms = Table(
    "rooms",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("room_group_id", Integer, ForeignKey("room_groups.id"), nullable=False),
    Column("name", String, nullable=False),
)

# Positions (Positionen)
positions = Table(
    "positions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=False),
    Column("name", String, nullable=False),
)

# Systems table
systems = Table(
    "systems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=False),
    Column("name", String, nullable=False),
)

# Devices table
devices = Table(
    "devices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("system_id", Integer, ForeignKey("systems.id"), nullable=False),
    Column("object_id", Integer, ForeignKey("objects.id"), nullable=True),
    Column("area_id", Integer, ForeignKey("areas.id"), nullable=True),
    Column("room_group_id", Integer, ForeignKey("room_groups.id"), nullable=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=True),
    Column("position_id", Integer, ForeignKey("positions.id"), nullable=True),
    Column("name", String, nullable=False),
    Column("device_type", String, nullable=False),
)

# Ports table
ports = Table(
    "ports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("direction", String, nullable=False),
    Column("connectivity", String, nullable=False),
    Column("connector_type", String, nullable=True),
    Column("signal_type", String, nullable=True),
)

# Connections table
connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("from_device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("from_port_id", Integer, ForeignKey("ports.id"), nullable=False),
    Column("to_device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("to_port_id", Integer, ForeignKey("ports.id"), nullable=False),
    Column("cable_type", String, nullable=True),
    Column("cable_length", Float, nullable=True),
)
