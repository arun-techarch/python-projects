# FastAPI Project Setup Guide

This guide provides step-by-step instructions for creating and setting up a FastAPI project using a virtual environment.

### 🚀 Project Creation
---

Follow these steps to create a new project from scratch:
1. Create a new project folder

    ```sh
    mkdir simple-api
    cd simple-api
    ```
2. Create and activate a virtual environment

    ```sh
    python -m venv pyenv
    pyenv/Scripts/activate     # Windows
    # source pyenv/bin/activate # Linux / MacOS
    ```
3. Upgrade pip to the latest version
    ```sh
    python -m pip install --upgrade pip
    ```
4. Install project dependencies
    ```sh
    pip install uvicorn[standard] fastapi
    ```
5. Save dependencies to requirements.txt
    ```sh
    pip freeze > requirements.txt
    ```
### 🔧 Project Setup (from GitHub)
---
1. Clone the repository
    ```sh
    git clone <github_repo>
    cd project_folder
    ```
2. Create and activate a virtual environment
    ```sh
    python -m venv pyenv
    pyenv/Scripts/activate     # Windows
    # source pyenv/bin/activate # Linux / MacOS
    ```
3. Upgrade pip to the latest version
    ```sh
    python -m pip install --upgrade pip
    ```
4. Install dependencies from requirements.txt
    ```sh
    pip install -r requirements.txt
    ```

### Running the API with Uvicorn
---

Run the following in terminal:
```sh
uvicorn app:app --reload --host 0.0.0.0 --port 8000 (dev)
uvicorn app:app --host 0.0.0.0 --port 8000 (prod)
```

* app:app → first app is the filename (app.py), second app is the FastAPI instance.
* --reload → auto-reload when you change code (useful for development).
* --host 0.0.0.0 → makes it accessible on local network.
* --port 8000 → sets the port.

### API Testing
---
* Open http://127.0.0.1:8000
 → root endpoint
* Open http://127.0.0.1:8000/docs
 → interactive Swagger UI


```sh
GET http://127.0.0.1:8000/

Response:
{
  "message": "Welcome to FastAPI running with Uvicorn!"
}
```
```sh
GET http://127.0.0.1:8000/hello/{name}

Example:
http://127.0.0.1:8000/hello/Arun 

Response:
{
  "message": "Hello, Arun!"
}
```
```sh
POST http://127.0.0.1:8000/items/

Payload:
{
  "id": 1,
  "name": "Laptop",
  "price": 30000.50,
  "in_stock": true
}

Response:
{
  "message": "Item created successfully",
  "item": {
    "id": 1,
    "name": "Laptop",
    "price": 30000.5,
    "in_stock": true
  }
}
```
```sh
PUT http://127.0.0.1:8000/items/{id}

Example:
http://127.0.0.1:8000/items/1

Payload:
{
  "id": 1,
  "name": "Laptop",
  "price": 40000.50,
  "in_stock": true
}

Response:
{
  "message": "Item 1 updated successfully",
  "item": {
    "id": 1,
    "name": "Laptop",
    "price": 40000.5,
    "in_stock": true
  }
}
```
```sh
GET http://127.0.0.1:8000/items/{id}

Example:
http://127.0.0.1:8000/items/1

Response:
{
  "message": "Item 1 retrieved successfully",
  "item": {
    "id": 1,
    "name": "Laptop",
    "price": 40000.5,
    "in_stock": true
  }
}
```
```sh
GET http://127.0.0.1:8000/items

Response:
{
  "message": "All Items retrieved successfully",
  "items": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 40000.5,
      "in_stock": true
    },
    {
      "id": 2,
      "name": "Mobile",
      "price": 25000.5,
      "in_stock": true
    }
  ]
}
```
```sh
DELETE http://127.0.0.1:8000/items/{id}

Example:
http://127.0.0.1:8000/items/1

Response:
{
  "message": "Item 1 successfully removed",
  "item": {
    "id": 1,
    "name": "Laptop",
    "price": 40000.5,
    "in_stock": true
  }
}
```

> **Note:** The application uses in-memory storage. Data is **not persisted** and will be lost upon application restart.
