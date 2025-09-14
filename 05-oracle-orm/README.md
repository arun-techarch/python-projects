## API Development with Oracle DB Integration using ORM(Object Relational Model)
This project demonstrates the setup and integration of an Oracle Database with an application backend, including ORM-based table creation, initial data loading, structured logging, and API testing.

Key Features & Steps
- Oracle DB Setup – Configure and connect to an Oracle Database instance.
- ORM Table Creation – Define and generate database tables using an Object-Relational Mapping (ORM) framework.
- Initial Data Seeding – Load predefined values into the tables to bootstrap the application.
- Application Logging – Implement structured logging for monitoring and debugging.
- API Testing – Validate endpoints and workflows using Postman collections.

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
uvicorn app.main:app
```

### 4. Test the API

This document provides example usage of the **API** with supported endpoints, request payloads, and response formats. The below API testing can be performed using Postman tool 

* Base URL: http://127.0.0.1:8000

#### 1. Get All Users

```http
GET /users/

Response:
[
    {
        "id": 1,
        "name": "Alice Johnson",
        "gender": "Female",
        "email": "alice@example.com",
        "country": "India",
        "age": 28,
        "phone": "+91-9000000001",
        "city": "Bengaluru"
    },
    {
        "id": 2,
        "name": "Bob Kumar",
        "gender": "Male",
        "email": "bob@example.com",
        "country": "India",
        "age": 35,
        "phone": "+91-9000000002",
        "city": "Chennai"
    },
    {
        "id": 3,
        "name": "Cathy Lee",
        "gender": "Female",
        "email": "cathy@example.com",
        "country": "India",
        "age": 22,
        "phone": "+91-9000000003",
        "city": "Mumbai"
    },
    {
        "id": 4,
        "name": "Daniel Smith",
        "gender": "Male",
        "email": "daniel@example.com",
        "country": "India",
        "age": 41,
        "phone": "+91-9000000004",
        "city": "Delhi"
    },
    {
        "id": 5,
        "name": "Eva Green",
        "gender": "Female",
        "email": "eva@example.com",
        "country": "India",
        "age": 30,
        "phone": "+91-9000000005",
        "city": "Hyderabad"
    }
]
```

#### 2. Get User by ID
```sh
GET /users/{id}

Example:
GET /users/3

Response:
{
    "name": "Cathy Lee",
    "age": 22,
    "gender": "Female",
    "phone": "+91-9000000003",
    "email": "cathy@example.com",
    "city": "Mumbai",
    "country": "India",
    "id": 3
}
```
#### 3. Create a User
```sh
POST /users/

Payload:
{
    "name": "Arun Stephen",
    "age": 30,
    "gender": "Male",
    "phone": "+91-9000000006",
    "email": "arun@example.com",
    "city": "Marthandam",
    "country": "India"
}

Response:
{
    "name": "Arun Stephen",
    "age": 30,
    "gender": "Male",
    "phone": "+91-9000000006",
    "email": "arun@example.com",
    "city": "Marthandam",
    "country": "India",
    "id": 6
}
```
#### 4. Update a User
```sh
PUT /users/{id}

Example:
PUT /users/6

Payload:
{
    "name": "Arun Stephen",
    "age": 30,
    "gender": "Male",
    "phone": "+91-9000000076",
    "email": "arun@example.com",
    "city": "Chennai",
    "country": "India"
}

Response:
{
    "name": "Arun Stephen",
    "age": 30,
    "gender": "Male",
    "phone": "+91-9000000076",
    "email": "arun@example.com",
    "city": "Chennai",
    "country": "India",
    "id": 6
}
```
#### 5. Delete a Product
```sh
DELETE /users/{id}

Example:
DELETE /users/6

Response:
Empty
```