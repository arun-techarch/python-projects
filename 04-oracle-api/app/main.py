import logging
from fastapi import FastAPI
from app.logger import setup_logging
from app.routers import products, reviews

app = FastAPI(title="Product Review API")

setup_logging()
logger = logging.getLogger("main")

# Routers
app.include_router(products.router)
app.include_router(reviews.router)

# Run with: uvicorn app.main:app --reload