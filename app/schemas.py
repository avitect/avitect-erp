from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

# --- User-Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None

# --- Customer-Schemas ---
class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

# --- Object-Schemas ---
class ObjectBase(BaseModel):
    customer_id: int
    name: str
    description: Optional[str] = None

class ObjectCreate(ObjectBase):
    pass

class ObjectRead(ObjectBase):
    id: int
    class Config:
        orm_mode = True

class ObjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# --- Bereich-Schemas ---
class AreaBase(BaseModel):
    object_id: int
    name: str

class AreaCreate(AreaBase):
    pass

class AreaRead(AreaBase):
    id: int
    class Config:
        orm_mode = True

class AreaUpdate(BaseModel):
    name: Optional[str] = None

# --- RoomGroup-Schemas ---
class RoomGroupBase(BaseModel):
    area_id: int
    name: str

class RoomGroupCreate(RoomGroupBase):
    pass

class RoomGroupRead(RoomGroupBase):
    id: int
    class Config:
        orm_mode = True

class RoomGroupUpdate(BaseModel):
    name: Optional[str] = None

# --- Room-Schemas ---
class RoomBase(BaseModel):
    area_id: int
    name: str

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int
    class Config:
        orm_mode = True

class RoomUpdate(BaseModel):
    name: Optional[str] = None

# --- Position-Schemas ---
class PositionBase(BaseModel):
    room_id: int
    name: str

class PositionCreate(PositionBase):
    pass

class PositionRead(PositionBase):
    id: int
    class Config:
        orm_mode = True

class PositionUpdate(BaseModel):
    name: Optional[str] = None

# --- System-Schemas ---
class SystemBase(BaseModel):
    object_id: int
    name: str

class SystemCreate(SystemBase):
    pass

class SystemRead(SystemBase):
    id: int
    class Config:
        orm_mode = True

class SystemUpdate(BaseModel):
    name: Optional[str] = None

# --- Device-Schemas ---
class DeviceBase(BaseModel):
    system_id: int
    name: str
    device_type: str
    object_id: Optional[int] = None
    area_id: Optional[int] = None
    roomgroup_id: Optional[int] = None
    room_id: Optional[int] = None
    position_id: Optional[int] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceRead(DeviceBase):
    id: int
    class Config:
        orm_mode = True

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    object_id: Optional[int] = None
    area_id: Optional[int] = None
    roomgroup_id: Optional[int] = None
    room_id: Optional[int] = None
    position_id: Optional[int] = None

# --- Port-Schemas ---
class PortBase(BaseModel):
    device_id: int
    name: str
    direction: Literal["input", "output"]
    connectivity: Literal["wired", "wireless"]
    connector_type: Optional[str] = None
    signal_type: Optional[str] = None

class PortCreate(PortBase):
    pass

class PortRead(PortBase):
    id: int
    class Config:
        orm_mode = True

class PortUpdate(BaseModel):
    name: Optional[str] = None
    direction: Optional[Literal["input", "output"]] = None
    connectivity: Optional[Literal["wired", "wireless"]] = None
    connector_type: Optional[str] = None
    signal_type: Optional[str] = None

# --- Connection-Schemas ---
class ConnectionBase(BaseModel):
    from_device_id: int
    from_port_id: int
    to_device_id: int
    to_port_id: int
    cable_type: Optional[str] = None
    cable_length: Optional[float] = None

class ConnectionCreate(ConnectionBase):
    pass

class ConnectionRead(ConnectionBase):
    id: int
    class Config:
        orm_mode = True

class ConnectionUpdate(BaseModel):
    cable_type: Optional[str] = None
    cable_length: Optional[float] = None
