from fastapi import APIRouter
from app.models.review import Review
from app.services import review_service

router = APIRouter(prefix="/products/{product_id}/reviews", tags=["Reviews"])

@router.post("/", response_model=dict)
def create_review(product_id: int, review: Review):
    review.product_id = product_id
    return review_service.create_review(review)

@router.get("/", response_model=list)
def get_reviews(product_id: int):
    return review_service.get_reviews_by_product(product_id)
