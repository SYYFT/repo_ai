# 📌 API Endpoints Documentation

## 1️⃣ **Check API Status**
### **`GET /`**
**Description:** Returns a simple message confirming the API is running.

📌 **Response:**
```json
{
  "message": "Welcome to the Repo Parser API!"
}
```

---

## 2️⃣ **Clone a GitHub Repository**
### **`POST /fetch-repo`**
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
- **500 Internal Server Error:** Git is not installed or repository cloning failed.
- **404 Not Found:** Repository does not exist.

---

## 3️⃣ **Parse a Cloned Repository**
### **`GET /parse/{repo_name}`**
**Description:** Parses a previously cloned repository and stores the results.

📌 **Path Parameter:**
- `repo_name` (string) - Name of the cloned repository

📌 **Response:**
```json
{
  "functions": ["def hello_world()"],
  "classes": ["class MyClass"],
  "dependencies": ["import os"]
}
```

📌 **Possible Errors:**
- **404 Not Found:** Repository not found.
- **500 Internal Server Error:** Parsing failed.

---

## 4️⃣ **Retrieve Parsed Data**
### **`GET /get_parsed_data`**
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
- **404 Not Found:** No parsed data available.

---

## 🛠️ **Error Handling**
| Error Code | Meaning |
|------------|---------|
| **400** | Bad Request (Invalid input) |
| **404** | Not Found (Missing resource) |
| **500** | Internal Server Error (Server failure) |

---

