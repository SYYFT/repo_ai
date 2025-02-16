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

## ✅ **You’re Ready to Go!** 🚀
By following these steps, your **FastAPI backend** and **frontend** should be up and running smoothly!

Let me know if you run into any issues. 🎯

