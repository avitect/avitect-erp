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
