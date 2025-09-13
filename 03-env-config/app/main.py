from fastapi import FastAPI
from app.routers import customers

app = FastAPI(title="Product Review API")

# Routers
app.include_router(customers.router)

# Run with: uvicorn app.main:app --reload