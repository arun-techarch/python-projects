## Load Environment-Specific Config to Connect the Database

This guide provides step-by-step instructions to set up an Oracle database inside a Docker container. It demonstrates how to run two separate databases (Development and Production), configure connections for each environment, and dynamically load the correct configuration based on the environment parameter when starting the application with Uvicorn.

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

### 2. Create Dev and Prod Database Setup (Docker)
Minimal docker run for dev database (detached)
```sh
docker run -d -p 1521:1521 --name dev-db -e ORACLE_PASSWORD=Admin@123 gvenzl/oracle-free:latest
```
Minimal docker run for prod database (detached)
```sh
docker run -d -p 1522:1521 --name prod-db -e ORACLE_PASSWORD=Admin@456 gvenzl/oracle-free:latest
```
Create customer table for both dev and prod
```sh
CREATE TABLE customer (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);
```
Insert customer table records for dev environment
```sh
INSERT INTO customer (name, email, phone, company, city, country) VALUES 
('Alice Johnson', 'alice.johnson@example.com', '9876543210', 'TechSoft', 'Chennai', 'India'),
('Brian Smith', 'brian.smith@example.com', '2025550176', 'FinServe', 'New York', 'USA'),
('Catherine Lee', 'catherine.lee@example.com', '7700900800', 'EduCore', 'London', 'UK');
```
Insert customer table records for prod environment
```sh
INSERT INTO customer (name, email, phone, company, city, country) VALUES 
('David Miller', 'david.miller@example.com', '+61-412345678', 'HealthFirst', 'Sydney', 'Australia'),
('Emma Wilson', 'emma.wilson@example.com', '+91-9123456789', 'RetailHub', 'Mumbai', 'India'),
('Frank Garcia', 'frank.garcia@example.com', '+34-612345678', 'TravelWay', 'Madrid', 'Spain'),
('Grace Chen', 'grace.chen@example.com', '+86-13123456789', 'GreenEnergy', 'Beijing', 'China'),
('Henry Brown', 'henry.brown@example.com', '+1-4155550134', 'AgriGrow', 'San Francisco', 'USA'),
('Isabella Rossi', 'isabella.rossi@example.com', '+39-3123456789', 'DesignPro', 'Milan', 'Italy');
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

### 4. API testing for Dev and Prod
- For Dev environment we need to pass **dev** config while running the uvicorn server
    ```sh
    $env:ENV="dev"; uvicorn app.main:app
    ```
    Launch the [API Docs](http://127.0.0.1:8000/docs) to test the API it will connect to the dev database and fetch the 3 records as response for the API.

    ```sh
    GET http://127.0.0.1:8000/customers/
    
    Response:
    [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "phone": "9876543210",
            "company": "TechSoft",
            "city": "Chennai",
            "country": "India"
        },
        {
            "id": 2,
            "name": "Brian Smith",
            "email": "brian.smith@example.com",
            "phone": "2025550176",
            "company": "FinServe",
            "city": "New York",
            "country": "USA"
        },
        {
            "id": 3,
            "name": "Catherine Lee",
            "email": "catherine.lee@example.com",
            "phone": "7700900800",
            "company": "EduCore",
            "city": "London",
            "country": "UK"
        }
    ]
    ```
- For Prod environment we need to pass **prod** config while running the uvicorn server
    ```sh
    $env:ENV="prod"; uvicorn app.main:app
    ```
    Launch the [API Docs](http://127.0.0.1:8000/docs) to test the API it will connect to the prod database and fetch the 6 records as response for the API.
    ```sh
    GET http://127.0.0.1:8000/customers/

    Response:
    [
        {
            "id": 1,
            "name": "David Miller",
            "email": "david.miller@example.com",
            "phone": "+61-412345678",
            "company": "HealthFirst",
            "city": "Sydney",
            "country": "Australia"
        },
        {
            "id": 2,
            "name": "Emma Wilson",
            "email": "emma.wilson@example.com",
            "phone": "+91-9123456789",
            "company": "RetailHub",
            "city": "Mumbai",
            "country": "India"
        },
        {
            "id": 3,
            "name": "Frank Garcia",
            "email": "frank.garcia@example.com",
            "phone": "+34-612345678",
            "company": "TravelWay",
            "city": "Madrid",
            "country": "Spain"
        },
        {
            "id": 4,
            "name": "Grace Chen",
            "email": "grace.chen@example.com",
            "phone": "+86-13123456789",
            "company": "GreenEnergy",
            "city": "Beijing",
            "country": "China"
        },
        {
            "id": 5,
            "name": "Henry Brown",
            "email": "henry.brown@example.com",
            "phone": "+1-4155550134",
            "company": "AgriGrow",
            "city": "San Francisco",
            "country": "USA"
        },
        {
            "id": 6,
            "name": "Isabella Rossi",
            "email": "isabella.rossi@example.com",
            "phone": "+39-3123456789",
            "company": "DesignPro",
            "city": "Milan",
            "country": "Italy"
        }
    ]
    ```