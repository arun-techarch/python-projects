from pydantic import BaseModel
from typing import Optional

class Review(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    comment: str
    rating: int
    comment_by: str
