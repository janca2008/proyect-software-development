from fastapi import APIRouter, HTTPException
from models.person import CustomerBase, CustomerID
import data.customer as db

router = APIRouter()


@router.get("/", response_model=list[CustomerID])
def list_customers():
    return db.read_active_customers()


@router.get("/history/all")
def list_history():
    return db.read_history()


@router.get("/{customer_id}", response_model=CustomerID)
def get_customer(customer_id: int):
    customer = db.read_one_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer


@router.post("/", response_model=CustomerID, status_code=201)
def create_customer(customer: CustomerBase):
    return db.create_customer(customer)


@router.put("/{customer_id}", response_model=CustomerID)
def update_customer(customer_id: int, customer: CustomerBase):
    updated = db.update_customer(customer_id, customer)
    if updated is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return updated


@router.delete("/{customer_id}", response_model=CustomerID)
def delete_customer(customer_id: int):
    customer = db.delete_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer