from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import database
from app.models import customers
from app.schemas import CustomerCreate, CustomerRead
from app.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

# Create
@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(
    data: CustomerCreate, user=Depends(get_current_user)
):
    query = customers.insert().values(**data.dict())
    customer_id = await database.execute(query)
    return {**data.dict(), "id": customer_id}

# Read All
@router.get("/", response_model=List[CustomerRead])
async def list_customers(user=Depends(get_current_user)):
    rows = await database.fetch_all(customers.select())
    return rows

# Read One
@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(customer_id: int, user=Depends(get_current_user)):
    row = await database.fetch_one(customers.select().where(customers.c.id == customer_id))
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return row

# Delete
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, user=Depends(get_current_user)):
    await database.execute(customers.delete().where(customers.c.id == customer_id))
    return
