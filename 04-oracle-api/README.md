## Production-Ready FastAPI Application with Oracle Integration
This project provides a production-ready folder structure for building scalable and maintainable APIs using FastAPI. The application is modularized into configurations, routers, services, and centralized logging, ensuring clean separation of concerns and easy extensibility.

It supports a product and sub-resource API structure (e.g., reviews), with built-in data validation and persistence to an Oracle database.

Key features include:
- Organized project layout for production readiness
- Centralized logging for monitoring and debugging
- Product and review API endpoints
- Oracle database integration with data verification
- Interactive API documentation using Swagger (OpenAPI)
- Application execution via Uvicorn

### Steps Overview
1. Oracle DB Setup in Docker  
2. Database Schema - Product & Reviews Table  
3. Project Setup and Run the project  
4. Test the API 

### 1. Oracle Database Setup (Docker)

Follow the steps below to set up an Oracle Database using a lightweight Docker image.  
This approach allows you to start and stop the Oracle service on demand, avoiding the need to keep it running continuously on your system.

#### 1. Prerequisites
* Docker Desktop installed and running (or Docker + Podman/Colima on macOS Apple Silicon).
* Oracle SQL Developer installed on your host machine.
* A few GB of disk free for the image and data.

#### 2. Choosing an Oracle Docker image

Official Oracle images: Found at Oracle Container Registry or container-registry.oracle.com. Requires accepting Oracle license and (usually) an Oracle account. Official images may have different startup steps and naming.

Community images (recommended for quick local dev): <i>gvenzl/oracle-free</i> or <i>gvenzl/oracle-xe</i> available on Docker Hub. These are widely used for development, CI, and local testing and are well-documented.

#### 3. Pull the image
Community (Docker Hub):
```sh
docker pull gvenzl/oracle-free:latest
```

#### 4. Run the container
Minimal docker run (detached)
```sh
docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=your_password gvenzl/oracle-free:latest
```
* -d — detached
* -p 1521:1521 — Oracle listener port
* -e ORACLE_PASSWORD=... — sets the database admin password used for SYS, SYSTEM, and PDBADMIN in gvenzl images. (Some older docs mention ORACLE_PWD but current gvenzl Docker images accept ORACLE_PASSWORD / secrets), see docs.

#### With persistent named volume (recommended)
```sh
docker volume create oracle-data
```
```sh
docker run -d --name oracle-db \
-p 1521:1521 -e ORACLE_PASSWORD=your_password \
-v oracle-data:/opt/oracle/oradata \
gvenzl/oracle-free:latest
```

#### 5. Check logs & wait for readiness

Monitor logs until the database reports it is ready. Example:

```sh
docker logs -f oracle-db
```
#### 6. Connecting with Oracle SQL Developer
1. Open SQL Developer.
2. Right-click Connections → New Connection...
3. Fill the New/Select Database Connection dialog with:
    *  Connection Name: OracleFreeDocker (any name)
    * Username: SYSTEM (or PDBADMIN or another user you created)
    * Password: the value set in ORACLE_PASSWORD
    * Hostname: localhost (or the Docker host IP)
    * Port: 1521
    * Service Name: FREE (default pluggable DB for gvenzl images)

4. Click Test — you should see Status: Success.
5. Click Connect to open a SQL Worksheet.

#### 7. Clean up

Stop and remove container and volumes:
```sh
docker stop oracle-db
docker rm oracle-db
docker volume rm oracle-data
```

### 2. Database Schema - Product & Reviews Table

This schema is designed to manage products and their reviews.

### 📌 Tables

#### 1. PRODUCT Table

| Column Name | Data Type     | Constraints             | Description                        |
|-------------|--------------|-------------------------|------------------------------------|
| ID          | INT          | PRIMARY KEY, AUTO_INCREMENT | Unique product  |
| NAME        | VARCHAR(100) | NOT NULL                | Name of the product               |
| DESCRIPTION | TEXT         | NULLABLE                | Detailed description of product   |
| PRICE       | DECIMAL(10,2)| NOT NULL                | Price of the product              |

#### 2. PRODUCT_REVIEW Table

| Column Name | Data Type     | Constraints                                  | Description                          |
|-------------|--------------|----------------------------------------------|--------------------------------------|
| ID          | INT          | PRIMARY KEY, AUTO_INCREMENT                  | Unique review identifier             |
| COMMENTS    | TEXT         | NULLABLE                                     | Customer review comments             |
| RATING      | INT          | CHECK (1 <= RATING <= 5)                     | Rating score (1 to 5)                |
| COMMENT_BY  | VARCHAR(100) | NULLABLE                                     | Name of the reviewer                 |
| COMMENT_ON  | DATETIME     | DEFAULT CURRENT_TIMESTAMP                    | Timestamp when comment was created   |
| PRODUCT_ID  | INT          | FOREIGN KEY → PRODUCT(ID)                    | Associated product identifier        |

### 📌 Queries to create and populate the data into tables

#### SQL Table Creation:
```sh
-- PRODUCT table
CREATE TABLE PRODUCT (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NAME VARCHAR2(100) NOT NULL,
    DESCRIPTION VARCHAR2(200),
    PRICE NUMBER(10,2) NOT NULL
);

-- PRODUCT_REVIEW table
CREATE TABLE PRODUCT_REVIEW (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    COMMENTS VARCHAR2(250),
    RATING NUMBER CHECK (RATING BETWEEN 1 AND 5),
    COMMENT_BY VARCHAR2(150),
    COMMENT_ON TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRODUCT_ID NUMBER,
    CONSTRAINT fk_product FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(ID)
);
```

#### Insert Data Into Tables:
```sh
-- Insert into PRODUCT table
INSERT INTO PRODUCT (NAME, DESCRIPTION, PRICE) VALUES
('Laptop', 'High performance laptop with 16GB RAM', 75000.00),
('Smartphone', 'Latest Android smartphone with 5G', 35000.00),
('Headphones', 'Noise cancelling wireless headphones', 5000.00),
('Smartwatch', 'Fitness tracking smartwatch with GPS', 12000.00);

-- Insert into PRODUCT_REVIEW table
INSERT INTO PRODUCT_REVIEW (COMMENTS, RATING, COMMENT_BY, PRODUCT_ID) VALUES
('Amazing performance, totally worth it!', 5, 'Arun', 1),
('Battery life could be better', 3, 'Priya', 1),
('Super fast and smooth experience', 4, 'Rahul', 2),
('Great sound quality!', 5, 'Sneha', 3),
('Very comfortable to wear', 4, 'Karthik', 3),
('Perfect for workouts', 5, 'Divya', 4);
```

### 📌 Initial Data into PRODUCT and PRODUCT_REVIEW table

#### PRODUCT Table:
```sh
SELECT * FROM PRODUCT;
```

| ID | NAME       | DESCRIPTION                           | PRICE   |
|----|-----------|---------------------------------------|---------|
| 1  | Laptop     | High performance laptop with 16GB RAM | 75000.00|
| 2  | Smartphone | Latest Android smartphone with 5G     | 35000.00|
| 3  | Headphones | Noise cancelling wireless headphones  | 5000.00 |
| 4  | Smartwatch | Fitness tracking smartwatch with GPS  | 12000.00|

#### PRODUCT_REVIEW Table:
```sh
SELECT * FROM PRODUCT_REVIEW;
```

| ID | COMMENTS                         | RATING | COMMENT_BY | COMMENT_ON          | PRODUCT_ID |
|----|----------------------------------|--------|------------|---------------------|------------|
| 1  | Amazing performance, totally worth it! | 5      | Arun       | 2025-09-12 14:00:00 | 1 |
| 2  | Battery life could be better     | 3      | Priya      | 2025-09-12 14:05:00 | 1 |
| 3  | Super fast and smooth experience | 4      | Rahul      | 2025-09-12 14:10:00 | 2 |
| 4  | Great sound quality!             | 5      | Sneha      | 2025-09-12 14:12:00 | 3 |
| 5  | Very comfortable to wear         | 4      | Karthik    | 2025-09-12 14:15:00 | 3 |
| 6  | Perfect for workouts             | 5      | Divya      | 2025-09-12 14:20:00 | 4 |

### 3. Project Setup and Run the project
Clone the repository and set up the environment.

```bash
# Clone the project
git clone <project_repo>

# Navigate to project folder
cd <project_folder>

# Create virtual environment
python -m venv pyenv

# Activate the environment
# On Linux/Mac:
source pyenv/bin/activate
# On Windows:
pyenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the project
$env:ENV="dev"; uvicorn app.main:app
```

### 4. Test the API

This document provides example usage of the **API** with supported endpoints, request payloads, and response formats.

* Base URL: http://127.0.0.1:8000
* API Docs: http://127.0.0.1:8000/docs

#### 1. Get All Products

```http
GET /products/

Response:
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High performance laptop with 16GB RAM",
    "price": 75000
  },
  {
    "id": 2,
    "name": "Smartphone",
    "description": "Latest Android smartphone with 5G",
    "price": 35000
  },
  {
    "id": 3,
    "name": "Headphones",
    "description": "Noise cancelling wireless headphones",
    "price": 5000
  },
  {
    "id": 4,
    "name": "Smartwatch",
    "description": "Fitness tracking smartwatch with GPS",
    "price": 12000
  }
]
```

#### 2. Get Product by ID
```sh
GET /products/{id}

Example:

GET /products/1

Response:
{
  "id": 1,
  "name": "Laptop",
  "description": "High performance laptop with 16GB RAM",
  "price": 75000
}
```
#### 3. Create a Product
```sh
POST /products/

Payload:
{
  "id": 6,
  "name": "Textbook",
  "description": "Technical Skill Books",
  "price": 2000.80
}

Response:
{
  "id": 10,
  "name": "Textbook",
  "description": "Technical Skill Books",
  "price": 2000.8
}
```
#### 4. Update a Product
```sh
PUT /products/{id}

Payload:
{
  "id": 10,
  "name": "Python Book",
  "description": "Technical Skill Books",
  "price": 1500.0
}

Response:
{
  "updated_id": 10
}
```
#### 5. Delete a Product
```sh
DELETE /products/{id}

Response:
{
  "deleted_id": 10
}
```
#### 6. Add a Product Review
```sh
POST /products/{id}/reviews/

Payload:
{
  "comment": "The product was really good",
  "rating": 4,
  "comment_by": "Arun"
}

Response:
{
  "id": 7,
  "product_id": 9,
  "comment": "The product was really good",
  "rating": 4,
  "comment_by": "Arun"
}
```
#### 7. Get Reviews for a Product
```sh
GET /products/{id}/reviews/

Response:
[
  {
    "id": 7,
    "product_id": 9,
    "comment": "The product was really good",
    "rating": 4,
    "comment_by": "Arun"
  },
  {
    "id": 8,
    "product_id": 9,
    "comment": "The product was damage",
    "rating": 3,
    "comment_by": "Andrino"
  }
]
```