from fastapi import APIRouter
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["Customer"])

@router.get("/", response_model=list)
def get_all_customers():
    return customer_service.get_all_customers()
