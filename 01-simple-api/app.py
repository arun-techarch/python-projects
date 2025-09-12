# app.py
from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI(title="Sample FastAPI with Uvicorn", version="1.0.0")
items = []

# Define request model
class Item(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI running with Uvicorn!"}


# Dynamic path parameter
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


# GET all items 
@app.get("/items")
def get_items():
    if len(items) > 0:
        return {"message": "All Items retrieved successfully", "items": items}
    else:
        return {"message": "No items found", "items": []}


# find the item from array using id
def find_index(id: int):
    return [item for item in items if item.id == id][0]   


# GET the item with specific id
@app.get("/items/{id}")
def get_items(id: int):
    item = find_index(id)
    if item:
        return {"message": f"Item {id} retrieved successfully", "item": item}
    else:
        return {"message": f"No item found with id {id}", "item": {}}


# POST request with body validation
@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item created successfully", "item": item}


# Update the item with specific id 
@app.put("/items/{id}")
def update_item(id: int, item: Item):
    updateItem = find_index(id)
    print(updateItem)
    if updateItem:
        updateItem.__dict__.update({'name': item.name, 'price': item.price, 'in_stock': item.in_stock})
        return {"message": f"Item {id} updated successfully", "item": updateItem}
    else:
        return {"message": f"No item found with id {id}", "item": {}}


# Update the item with specific id 
@app.delete("/items/{id}")
def delete_item(id: int):
    item = find_index(id)
    if item:
        items.remove(item)
        return {"message": f"Item {id} successfully removed", "item": item}
    else:
         return {"message": f"No item found with id {id}", "item": {}}