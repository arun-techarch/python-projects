## Automated Data Processing and Reporting using Scheduled Job in Python

This project demonstrates three practical scenarios of scheduled job automation using Python. It focuses on reducing manual intervention, improving efficiency, and enabling seamless data handling across databases and files. The automation workflows include database synchronization, bulk data ingestion, and scheduled reporting with email notifications.

1. Database Synchronization (Source → Target)
    - Copies table data from a source database to a target database at scheduled intervals.
    - If the target table does not exist, it will be created automatically.
    - Ensures the latest data is always synchronized without manual effort.
    - Includes optional email notifications for success or failure with detailed error messages.

2. Bulk Data Load from CSV to Database
    - Reads data from CSV files and dynamically creates tables and columns if required.
    - Supports bulk upload and data updates into the target database.
    - Can process files from a shared folder or directory.
    - Scheduled execution eliminates the need for manual uploads.
    - Sends completion or error notification via email.

3. Automated Report Generation and Email Delivery
    - Fetches data from the database and formats it into a predefined report structure.
    - Automatically sends the report via email to clients or stakeholders.
    - Can be scheduled to provide insights, KPIs, or metrics at regular intervals.

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

### 2. Create Source and Target Database Setup (Docker)
Minimal docker run for source database (detached)
```sh
docker run -d -p 1521:1521 --name source-db -e ORACLE_PASSWORD=Admin@123 gvenzl/oracle-free:latest
```
Minimal docker run for target database (detached)
```sh
docker run -d -p 1522:1521 --name target-db -e ORACLE_PASSWORD=Admin@456 gvenzl/oracle-free:latest
```
Create customer table in source database
```sh
-- Create CUSTOMER table
CREATE TABLE CUSTOMER (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);
```
Insert customer table records into source database
```sh
-- Insert 20 sample records
INSERT INTO CUSTOMER (id, name, email, phone, company, city, country) VALUES
(1, 'John Smith', 'john.smith@example.com', '+1-202-555-0101', 'TechCorp', 'New York', 'USA'),
(2, 'Alice Johnson', 'alice.johnson@example.com', '+44-20-7946-0958', 'FinServe', 'London', 'UK'),
(3, 'Ravi Kumar', 'ravi.kumar@example.com', '+91-9876543210', 'InnoSoft', 'Bangalore', 'India'),
(4, 'Maria Garcia', 'maria.garcia@example.com', '+34-91-123-4567', 'HealthPlus', 'Madrid', 'Spain'),
(5, 'Chen Wei', 'chen.wei@example.com', '+86-10-5555-7890', 'DragonTech', 'Beijing', 'China'),
(6, 'James Brown', 'james.brown@example.com', '+1-415-555-0123', 'CloudNet', 'San Francisco', 'USA'),
(7, 'Emma Wilson', 'emma.wilson@example.com', '+61-2-9876-5432', 'EduGlobal', 'Sydney', 'Australia'),
(8, 'Oliver Davis', 'oliver.davis@example.com', '+64-9-555-7788', 'AgriCorp', 'Auckland', 'New Zealand'),
(9, 'Sophia Müller', 'sophia.mueller@example.com', '+49-30-123456', 'GreenEnergy', 'Berlin', 'Germany'),
(10, 'Lucas Silva', 'lucas.silva@example.com', '+55-11-99887766', 'FoodMart', 'São Paulo', 'Brazil'),
(11, 'Fatima Ali', 'fatima.ali@example.com', '+971-4-22334455', 'SmartLogistics', 'Dubai', 'UAE'),
(12, 'David Lee', 'david.lee@example.com', '+82-2-777-8888', 'FutureAI', 'Seoul', 'South Korea'),
(13, 'Isabella Rossi', 'isabella.rossi@example.com', '+39-06-9876543', 'DesignHub', 'Rome', 'Italy'),
(14, 'Ahmed Hassan', 'ahmed.hassan@example.com', '+20-2-23456789', 'BuildTech', 'Cairo', 'Egypt'),
(15, 'William Taylor', 'william.taylor@example.com', '+1-312-555-0199', 'SecureNet', 'Chicago', 'USA'),
(16, 'Nora Svensson', 'nora.svensson@example.com', '+46-8-1234567', 'MediCare', 'Stockholm', 'Sweden'),
(17, 'Hiroshi Tanaka', 'hiroshi.tanaka@example.com', '+81-3-2345-6789', 'AutoMoto', 'Tokyo', 'Japan'),
(18, 'Carlos Lopez', 'carlos.lopez@example.com', '+52-55-7654321', 'RetailPro', 'Mexico City', 'Mexico'),
(19, 'Elena Petrova', 'elena.petrova@example.com', '+7-495-1234567', 'BankTrust', 'Moscow', 'Russia'),
(20, 'Michael Johnson', 'michael.johnson@example.com', '+1-213-555-0188', 'NextGenTech', 'Los Angeles', 'USA');
```

### ✅ Gmail configuration for sending the mail
1. Step 1: Enable 2FA on your Gmail
    - Go to Google [Account Security](https://myaccount.google.com/u/1/security)
    - Turn on 2-Step Verification.

2. Step 2: Generate an App Password
    - In the same security page → App passwords.
    - Select app: Mail, select device: Other (give any name).
    - Google generates a 16-character password (looks like abcd efgh ijkl mnop).

3. Step 3: Update your config.json
    - Instead of your real Gmail password, put the App Password and other configuration into config.json file

### 🔧 Project Setup (from GitHub)

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
5. Run the python application
    ```sh
    python ./app/main.py
    ```

### 🔑 Python Scheduler or Automation Use Cases:

- ETL Jobs → Copy/transform data between Oracle tables.
- Excel Automation → Read Excel and load to DB.
- Reporting → Extract data and email to stakeholders.
- Cleanup Tasks → Archive old records automatically.
- Monitoring → Run health checks and alert via mail.