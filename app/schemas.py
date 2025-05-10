from pydantic import BaseModel, EmailStr
from typing import Optional

# --- User-Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

# --- Customer-Schemas ---
class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int

from typing import Optional

# --- Object-Schemas ---
class ObjectBase(BaseModel):
    customer_id: int
    name: str
    description: Optional[str] = None

class ObjectCreate(ObjectBase):
    pass

class ObjectRead(ObjectBase):
    id: int

# --- Bereich-Schemas ---
class AreaBase(BaseModel):
    object_id: int
    name: str

class AreaCreate(AreaBase):
    pass

class AreaRead(AreaBase):
    id: int

# --- RoomGroup-Schemas ---
class RoomGroupBase(BaseModel):
    area_id: int
    name: str

class RoomGroupCreate(RoomGroupBase):
    pass

class RoomGroupRead(RoomGroupBase):
    id: int

# --- Room-Schemas ---
class RoomBase(BaseModel):
    area_id: int
    name: str

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

# --- Position-Schemas ---
class PositionBase(BaseModel):
    room_id: int
    name: str

class PositionCreate(PositionBase):
    pass

class PositionRead(PositionBase):
    id: int

# --- System-Schemas ---
class SystemBase(BaseModel):
    object_id: int
    name: str

class SystemCreate(SystemBase):
    pass

class SystemRead(SystemBase):
    id: int
