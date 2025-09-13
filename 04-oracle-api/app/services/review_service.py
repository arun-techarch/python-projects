import logging
from app.models.review import Review
from app.services.db import get_cursor

logger = logging.getLogger(__name__)

def create_review(review: Review):
    with get_cursor() as cur:
        out_id = cur.var(int)
        cur.execute(
            "INSERT INTO product_review (product_id, comments, rating, comment_by) VALUES (:1, :2, :3, :4) RETURNING id INTO :5",
            [review.product_id, review.comment, review.rating, review.comment_by, out_id]
        )
        review_id = out_id.getvalue()[0]
        logger.info(f"Product {review.product_id} of review {review_id} was created successfully")
        return {**review.dict(), "id": review_id}

def delete_review(review_id: int):
    with get_cursor() as cur:
        cur.execute("DELETE FROM reviews WHERE id=:1", [review_id])
        logger.info(f"Review {review_id} was removed successfully")
        return {"deleted_id": review_id}

def get_reviews_by_product(product_id: int):
    with get_cursor() as cur:
        cur.execute("SELECT id, product_id, comments, rating, comment_by FROM product_review WHERE product_id=:1", [product_id])
        rows = cur.fetchall()
        logger.info(f"All Reviews of product {product_id} was retrieved successfully")
        return [dict(zip(["id", "product_id", "comment", "rating", "comment_by"], row)) for row in rows]
