import logging
from app.services.db import get_cursor
from app.models.product import Product

logger = logging.getLogger(__name__)

def create_product(product: Product):
    try:
        with get_cursor() as cur:
            out_id = cur.var(int)
            cur.execute(
                "INSERT INTO product (name, description, price) VALUES (:1, :2, :3) RETURNING id INTO :4",
                [product.name, product.description, product.price, out_id]
            )
            product_id = out_id.getvalue()[0]
            logger.info(f"product {product_id} was created successfully")
            return {**product.dict(), "id": product_id}
    except Exception as e:
        print(e)

def get_product(product_id: int):
    with get_cursor() as cur:
        cur.execute("SELECT id, name, description, price FROM product WHERE id = :1", [product_id])
        row = cur.fetchone()
        logger.info(f"product {product_id} was retrieved successfully")
        return dict(zip(["id", "name", "description", "price"], row)) if row else None

def get_all_products():
    with get_cursor() as cur:
        cur.execute("SELECT id, name, description, price FROM product")
        rows = cur.fetchall()
        logger.info(f"All products are retrieved successfully")
        return [dict(zip(["id", "name", "description", "price"], row)) for row in rows]

def update_product(product_id: int, product: Product):
    with get_cursor() as cur:
        cur.execute(
            "UPDATE product SET name=:1, description=:2, price=:3 WHERE id=:4",
            [product.name, product.description, product.price, product_id]
        )
        logger.info(f"product {product_id} was updated successfully")
        return {"updated_id": product_id}

def delete_product(product_id: int):
    with get_cursor() as cur:
        # delete reviews first
        cur.execute("DELETE FROM product_review WHERE product_id=:1", [product_id])
        cur.execute("DELETE FROM product WHERE id=:1", [product_id])
        logger.info(f"product {product_id} was removed successfully")
        return {"deleted_id": product_id}
