from fastapi import APIRouter, HTTPException
from app.models.product import Product
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=dict)
def create_product(product: Product):
    return product_service.create_product(product)

@router.get("/{product_id}", response_model=dict)
def get_product(product_id: int):
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list)
def get_all_products():
    return product_service.get_all_products()

@router.put("/{product_id}", response_model=dict)
def update_product(product_id: int, product: Product):
    return product_service.update_product(product_id, product)

@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: int):
    return product_service.delete_product(product_id)
