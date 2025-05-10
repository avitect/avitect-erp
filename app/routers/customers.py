from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import database
from app.models import customers
from app.schemas import CustomerCreate, CustomerRead, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate):
    query = customers.insert().values(**customer.dict())
    customer_id = await database.execute(query)
    return {**customer.dict(), "id": customer_id}

@router.get("/", response_model=List[CustomerRead])
async def read_customers():
    query = customers.select()
    return await database.fetch_all(query)

@router.get("/{id}", response_model=CustomerRead)
async def read_customer(id: int):
    query = customers.select().where(customers.c.id == id)
    customer = await database.fetch_one(query)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer nicht gefunden",
        )
    return customer

@router.put("/{id}", response_model=CustomerRead)
async def update_customer(id: int, customer: CustomerUpdate):
    values = {k: v for k, v in customer.dict().items() if v is not None}
    query = (
        customers.update()
        .where(customers.c.id == id)
        .values(**values)
        .returning(customers)
    )
    updated = await database.fetch_one(query)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer nicht gefunden",
        )
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(id: int):
    query = customers.delete().where(customers.c.id == id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer nicht gefunden",
        )
    return None
