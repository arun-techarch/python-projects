# python-projects
🚀 A comprehensive Python learning and development playground covering end-to-end web and API development. This repository demonstrates how to build scalable applications with:

✅ Environment configuration & structured logging
✅ In-memory storage, RDBMS, and NoSQL databases
✅ ORM integrations for efficient data handling
✅ Message queues for async communication
✅ Flask-based websites and REST APIs with database support
✅ Task schedulers & dashboards for real-world workflows

Designed with multiple hands-on use cases, this repo is perfect for anyone looking to strengthen their skills in Python backend engineering and gain expertise in modern web development practices.

The primary prerequisite is Docker Desktop and Microsoft Visual Source Code, Python with an installation guide provided for Windows and external references for Linux and macOS. Each project repository includes its specific prerequisites and setup instructions to support testing. Finally, this repository enables building, deploying, and validating python projects.

> Docker Desktop

> Microsoft Visual Source Code

> Python

> RabbitMQ

> Apache Kafka

## Docker Desktop Installation Guide

This document provides step-by-step instructions to install **Docker Desktop** on **Windows**.  
For **Linux** and **macOS**, official installation documentation links are provided for reference.



## 📌 Prerequisites for Windows
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063 or later)  
  OR Windows 11 64-bit: Pro, Enterprise, or Education.  
- Enable **Hyper-V** and **Containers** features.  
- Ensure **WSL 2** (Windows Subsystem for Linux v2) is enabled (recommended).  
- Minimum:  
  - 4 GB RAM  
  - Virtualization enabled in BIOS  



## ⚙️ Steps to Install Docker Desktop on Windows

### 1. Download Docker Desktop Installer
- Go to the official Docker download page:  
  👉 [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

### 2. Run the Installer
- Double-click the downloaded `Docker Desktop Installer.exe`.  
- If prompted for permissions, click **Yes** to allow.

### 3. Choose Configuration Options
- During setup, ensure these options are selected (if available):
  - ✅ Use **WSL 2** instead of Hyper-V (recommended for Windows 10/11).  
  - ✅ Add shortcut to Desktop.

### 4. Complete Installation
- Click **OK** when prompted to enable WSL 2.  
- If WSL 2 is not already installed, follow the guided setup to install/update WSL 2.  
- Restart your computer if required.

### 5. Launch Docker Desktop
- Open **Docker Desktop** from Start Menu or Desktop shortcut.  
- Wait until the **Docker whale icon** in the system tray turns stable (no animation).  

### 6. Verify Installation
- Open **PowerShell** or **Command Prompt** and run:
  ```bash
  docker --version
  docker run hello-world

You should see Docker version details and a confirmation message that Docker is working correctly.



📦 Additional Configuration (Optional)
---

* Integrate with WSL 2 distributions:

    * Open Docker Desktop → Settings → Resources → WSL Integration.

    * Enable for the required Linux distributions.

* Enable Kubernetes (optional):

    * Docker Desktop → Settings → Kubernetes → Check Enable Kubernetes.

🔗 Installation Guides for Other Platforms
--

Linux (Ubuntu, Debian, Fedora, CentOS, etc.):
👉 [Docker Engine Installation on Linux](https://docs.docker.com/engine/install/)

macOS (Intel & Apple Silicon):
👉 [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

✅ Verification
---

- After installation on any platform, run:
  ```bash
  docker run hello-world

This confirms Docker is installed and functional.



## Microsoft Visual Studio Code Installation Guide

This guide provides detailed steps to install **Microsoft Visual Studio Code (VS Code)** on **Windows**.  
For **Linux** and **macOS**, official links are provided for reference.

---

## 📌 Prerequisites
- A system with internet connectivity
- Administrator access for installation

---

## 🖥️ Windows Installation

### Step 1: Download the Installer
1. Open your browser and go to the official VS Code download page:  
   👉 [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
2. Select **Windows** and download the installer (`.exe` file).

### Step 2: Run the Installer
1. Double-click the downloaded `VSCodeSetup-x64-x.x.x.exe` file.
2. If prompted by **User Account Control (UAC)**, click **Yes** to allow installation.

### Step 3: Accept the License Agreement
- Read and accept the **license agreement**.
- Click **Next** to proceed.

### Step 4: Select Destination Location
- Default path:  

C:\Users<YourUsername>\AppData\Local\Programs\Microsoft VS Code

- You can change the path if required, then click **Next**.

### Step 5: Select Additional Tasks
- Check the following recommended options:
- ✅ Create a desktop icon  
- ✅ Add "Open with Code" action to Windows Explorer  
- ✅ Add to PATH (important for using `code` command in terminal)  

Click **Next**.

### Step 6: Install
- Click **Install** to start the installation process.
- Wait until the progress bar completes.

### Step 7: Launch VS Code
- Check **Launch Visual Studio Code** before clicking **Finish**.
- Alternatively, open it later from the **Start Menu** or Desktop shortcut.


## 🐧 Linux Installation
Follow the official guide here:  
👉 [Install VS Code on Linux](https://code.visualstudio.com/docs/setup/linux)


## 🍏 macOS Installation
Follow the official guide here:  
👉 [Install VS Code on macOS](https://code.visualstudio.com/docs/setup/mac)


## ✅ Verification
1. Open a terminal (Command Prompt / PowerShell).
2. Type:
 ```bash
 code --version
 ```

## Python Installation Guide

This guide provides step-by-step instructions to install **Python** on different operating systems.  


## 🖥️ Python Installation

### Step 1: Download Python
1. Visit the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Download the latest stable release (e.g., Python 3.x.x).
   - Choose the correct installer based on your system:
     - `Windows Installer (64-bit)`
     - `Windows Installer (32-bit)`

---

### Step 2: Run the Installer
1. Double-click the downloaded installer (`python-3.x.x-amd64.exe`).
2. On the setup screen:
   - ✅ **Check the box**: *"Add Python 3.x to PATH"*
   - Click **Install Now** (recommended)  
     *(Alternatively, choose "Customize Installation" for advanced setup options.)*

---

### Step 3: Verify Installation
1. Open **Command Prompt** (`Win + R`, type `cmd`, and press Enter).
2. Run the following command to verify Python is installed:

   ```sh
   python --version
   ```
   You should see the installed version, e.g.:
   ```sh
   Python 3.12.1
   ```
3. Verify pip (Python package manager) installation:
    ```sh
    pip --version
    ```

### Step 4: Upgrade pip (Optional but Recommended)
---
```sh
python -m pip install --upgrade pip
```

### Step 5: Test Installation
---
To verify that Python is installed and working correctly using **Visual Studio Code (VS Code)**, follow the steps below.


### 1. Open Visual Studio Code
- Launch **VS Code** from your Start Menu or Desktop.

### 2. Create a Test Python File
1. In VS Code, click **File > New File**.  
2. Save the file as **test.py**.  
   - Example: `C:\Users\<YourName>\Documents\test.py`

### 3. Add Test Script
Type the following Python code inside `test.py`:

```python
print("Hello, Python is installed successfully!")
```

### 4. Run the Script in VS Code
#### Option A: Using the Integrated Terminal
* Open the Terminal inside VS Code:
    * Menu: View > Terminal
    * Or shortcut: Ctrl + `
* In the terminal, run:
    ```sh
    python test.py
    ```
* You should see the output:
    ```sh
    Hello, Python is installed successfully!
    ```

#### Option B: Using the "Run Python File" Button
* Click the Run ▶ button at the top-right corner of the editor.
* Output will appear in the Terminal/Output panel.

## 🐧 Python Installation in Linux

For Linux installation steps, please refer to the official documentation:
👉 [Python Linux Installation Guide](https://docs.python.org/3/using/unix.html)

## 🍎 Python Installation in macOS

For macOS installation steps, please refer to the official documentation:
👉 [Python macOS Installation Guide](https://docs.python.org/3/using/mac.html)