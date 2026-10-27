from fastapi import APIRouter, HTTPException
from models.product import ProductBase, ProductID
import data.product as db
from enums.status import Status

router = APIRouter()


@router.get("/", response_model=list[ProductID])
def list_products():
    return db.read_active_products()


@router.get("/history/all")
def list_history():
    return db.read_history()
@router.get("/search", response_model=list[ProductID])
def search_products(
    name: str | None = None,
    description: str | None = None,
    department: str | None = None,
    category: str | None = None,
    status: Status | None = None,
    min_starting_price: float | None = None,
    max_starting_price: float | None = None,
    min_finish_price: float | None = None,
    max_finish_price: float | None = None,
):
    return db.filter_products(
        name=name,
        description=description,
        department=department,
        category=category,
        status=status,
        min_starting_price=min_starting_price,
        max_starting_price=max_starting_price,
        min_finish_price=min_finish_price,
        max_finish_price=max_finish_price,
    )


@router.get("/{product_id}", response_model=ProductID)
def get_product(product_id: int):
    product = db.read_one_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.post("/", response_model=ProductID, status_code=201)
def create_product(product: ProductBase):
    return db.create_product(product)


@router.put("/{product_id}", response_model=ProductID)
def update_product(product_id: int, product: ProductBase):
    updated = db.update_product(product_id, product)
    if updated is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated


@router.delete("/{product_id}", response_model=ProductID)
def delete_product(product_id: int):
    product = db.delete_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product