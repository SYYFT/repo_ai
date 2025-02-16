# 📘 Repo API Documentation

## Overview
The **Repo API** is a FastAPI-based service that allows users to:
- Clone GitHub repositories
- Retrieve the file structure of a repository
- Parse repository contents
- Fetch previously parsed data

## 🚀 Base URL
```
http://localhost:8000
```

## 📌 Endpoints

### 1️⃣ **Root - Check API Status**
#### **`GET /`**
**Description:** Confirms the API is running.

📌 **Response:**
```json
{
  "message": "Welcome to the Repo Parser API!"
}
```

---
### 2️⃣ **Fetch a GitHub Repository**
#### **`POST /fetch-repo`**
**Description:** Clones a GitHub repository and returns its file structure.

📌 **Request Body:**
```json
{
  "repo_url": "https://github.com/example/repo.git"
}
```

📌 **Response:**
```json
{
  "repo_name": "repo",
  "files": ["README.md", "src/main.py", "src/utils.py"]
}
```

📌 **Possible Errors:**
- **500 Internal Server Error**: Git is not installed or repository cloning failed.
- **404 Not Found**: Repository does not exist.

---
### 3️⃣ **Parse a Cloned Repository**
#### **`GET /parse/{repo_name}`**
**Description:** Parses a previously cloned repository and stores the results.

📌 **Path Parameter:**
- `repo_name` (string) - Name of the cloned repo

📌 **Response:**
```json
{
  "functions": ["def hello_world()"],
  "classes": ["class MyClass"],
  "dependencies": ["import os"]
}
```

📌 **Possible Errors:**
- **404 Not Found**: Repository not found.
- **500 Internal Server Error**: Parsing failed.

---
### 4️⃣ **Retrieve Parsed Data**
#### **`GET /get_parsed_data`**
**Description:** Returns the most recently parsed repository data.

📌 **Response:**
```json
{
  "functions": ["def fetch_repo()"],
  "classes": ["class RepoHandler"],
  "dependencies": ["import requests"]
}
```

📌 **Possible Errors:**
- **404 Not Found**: No parsed data available.

---
## ⚙️ Setup & Running Locally
### **📌 Installation**
1. Clone the repository:
   ```sh
   git clone https://github.com/your/repo-api.git
   cd repo-api
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the API:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Open API docs in your browser:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Redoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
## 🛠️ Error Handling
| Error Code | Meaning |
|------------|---------|
| **400** | Bad Request (Invalid input) |
| **404** | Not Found (Missing resource) |
| **500** | Internal Server Error (Server failure) |

---
## 🔗 Future Enhancements
- **Authentication for private repositories**
- **Support for Bitbucket & GitLab**
- **Graphical UI for repo parsing insights**

---
## 📌 Author
🚀 Created by **Your Name** | GitHub: [your-profile](https://github.com/your-profile)

---

---
## DEBUGGING AND CONFIGURATION 

# 🚀 Setting Up and Running Repo API

This document provides step-by-step instructions on how to set up and run the **Repo API** in a GitHub Codespace.

---

## **1️⃣ Kill Any Process Using Port 8000**
Before starting the server, ensure that no other process is using **port 8000**.

### **🔍 Find and Kill the Process**
Run the following command to check if port `8000` is occupied:
```sh
lsof -i :8000
```
If a process is using port `8000`, terminate it with:
```sh
lsof -ti :8000 | xargs kill -9
```
Verify that the port is now free:
```sh
lsof -i :8000
```
If no output appears, the port is successfully freed.

---

## **2️⃣ Start the FastAPI Server with Uvicorn**
Once the port is available, start the **FastAPI backend** using Uvicorn.

### **🔍 Navigate to the Backend Directory**
Make sure you are in the correct directory:
```sh
cd /workspaces/repo_ai
```

### **🔍 Run the FastAPI Server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

If port `8000` is still in use, try using another port (e.g., `8080`):
```sh
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

---

## **3️⃣ Access API Documentation**
FastAPI provides automatic documentation that can be accessed in the browser:

✅ **Swagger UI (Interactive API Testing)**
👉 `https://your-codespace-username-8000.preview.app.github.dev/docs`

✅ **Redoc UI (Structured API Reference)**
👉 `https://your-codespace-username-8000.preview.app.github.dev/redoc`

(If running on another port, replace `8000` with your actual port.)

---

## **4️⃣ Start the Frontend Application**
If a frontend is included, follow these steps:

### **🔍 Navigate to the Frontend Directory**
```sh
cd frontend  # Adjust if needed
```

### **🔍 Start the Frontend Server**
```sh
npm run dev
```

✅ **Frontend should be accessible at:**
👉 `https://your-codespace-username-3000.preview.app.github.dev/`

---

## **5️⃣ Debugging & Common Fixes**
| Issue | Fix |
|-------|-----|
| `Address already in use` | Run `lsof -ti :8000 | xargs kill -9` to free the port |
| `Failed to fetch` (Frontend) | Ensure FastAPI is running at the correct URL |
| `404 Not Found` | Verify the endpoint exists in `main.py` |

---

## 🔍 Correct Understanding of CORS

Backend (FastAPI) → Runs on 8000
URL: https://effective-guacamole-4pjwr7qv4j7fjqvv-8000.app.github.dev
Frontend (React/Vite) → Runs on 5173
URL: https://effective-guacamole-4pjwr7qv4j7fjqvv-5173.app.github.dev
✅ The backend CORS settings must allow requests coming from the frontend (5173), so the backend must "whitelist" the frontend URL

