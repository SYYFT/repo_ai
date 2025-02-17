import os
import sys
import json
import stat
import shutil
import subprocess
import logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ✅ Ensure the `parser/` directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "parser")))
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Import `parser.py` correctly
try:
    import parser

except ImportError:
    raise HTTPException(status_code=500, detail="Failed to import `parser.py`. Check file location.")

# ✅ Initialize FastAPI
app = FastAPI()

# ============================
# 📌 CORS Configuration
# ============================
CODESPACE_NAME = os.environ.get("CODESPACE_NAME")

if CODESPACE_NAME:
    FRONTEND_URL = f"https://{CODESPACE_NAME}-*.app.github.dev"  # Allow dynamic frontend ports
else:
    FRONTEND_URL = "http://localhost:5173"  # Default for local development

print(f"✅ CORS allowed origin set to: {FRONTEND_URL}")  # Debugging

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Dynamically set frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # ✅ Restrict methods for security
    allow_headers=["*"],  # Allow all headers
)

# ============================
# 📌 Models for API Requests
# ============================
class RepoRequest(BaseModel):
    """Request model for fetching GitHub repository."""
    repo_url: str

# ============================
# 📌 Utility Functions
# ============================
BASE_CLONE_DIR = "cloned_repos"


def remove_readonly(func, path, exc_info):
    """Helper function to remove read-only files on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_existing_repo(repo_path: str):
    """Remove an existing repository before cloning."""
    if os.path.exists(repo_path):
        try:
            shutil.rmtree(repo_path, onerror=remove_readonly)
            print(f"✅ Deleted existing repo: {repo_path}")
        except PermissionError as e:
            print(f"❌ Permission Error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to delete repo: {e}")



def check_git_installed():
    """Ensure Git is installed on the system."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Git is not installed. Please install Git.")

def clone_github_repo(repo_url: str, repo_path: str):
    """Clone a GitHub repository to a local directory."""
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            capture_output=True, text=True, check=True
        )
        print("✅ Git Clone Success:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Git Clone Error:", e.stderr)
        raise HTTPException(status_code=500, detail=f"Git Clone Failed: {e.stderr}")

def list_repository_files(repo_path: str):
    """Return a list of all files inside the cloned repository."""
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail="Repository not found")
    
    file_list = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), repo_path))
    return file_list

def parse_and_save_repo(repo_path: str):
    """Parse repository using `parser.py` and save the result."""
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail="Repository not found")

    parsed_data = parser.parse_repository(repo_path)

    with open("parsed_repo.json", "w") as json_file:
        json.dump(parsed_data, json_file, indent=4)

    return parsed_data

# ============================
# 📌 API Endpoints
# ============================
@app.get("/")
def root():
    """Root endpoint to confirm API is running."""
    return {"message": "Welcome to the Repo Parser API!"}

@app.post("/fetch-repo")
async def fetch_repo(request: RepoRequest):
    """Clone a GitHub repository and return its file structure."""
    repo_url = request.repo_url
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(BASE_CLONE_DIR, repo_name)

    print(f"🔍 Fetching repository: {repo_url}")

    # ✅ Check if Git is installed
    check_git_installed()

    # ✅ Remove existing repo if it exists
    clean_existing_repo(repo_path)

    # ✅ Clone the repository
    try:
        clone_github_repo(repo_url, repo_path)
    except HTTPException as e:
        return {"error": str(e.detail)}

    # ✅ Retrieve file list
    try:
        files = list_repository_files(repo_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {e}")

    return {"repo_name": repo_name, "files": files}

@app.get("/parse/{repo_name}")
def parse_repository_api(repo_name: str):
    """Trigger parsing of a repository and return parsed JSON data."""
    repo_path = os.path.join(BASE_CLONE_DIR, repo_name)

    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail=f"Repository '{repo_name}' not found.")

    # ✅ Parse and save data
    try:
        parsed_data = parse_and_save_repo(repo_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while parsing repository: {e}")

    return parsed_data



@app.get("/get_parsed_data")
def get_parsed_data():
    """Return the latest parsed repository data from the JSON file in a pretty format."""
    json_file = "parsed_repo.json"

    if not os.path.exists(json_file):
        raise HTTPException(status_code=404, detail="❌ No parsed data available. Run /parse/{repo_name} first.")

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            parsed_data = json.load(f)  # ✅ Properly loads JSON file
        return JSONResponse(content=parsed_data, media_type="application/json", indent=4)
    
    except json.JSONDecodeError as e:
        logging.error(f"❌ JSON Decode Error: {e}")
        raise HTTPException(status_code=500, detail="❌ Corrupted JSON file. Try re-parsing the repository.")

    except Exception as e:
        logging.error(f"❌ Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Internal Server Error: {e}")


@app.options("/fetch-repo")
async def options_handler():
    """Handle preflight OPTIONS request for CORS."""
    return {"message": "Preflight request accepted"}

@app.get("/test")
def test_api():
    """Test API to confirm backend is reachable."""
    return {"message": "Hello from FastAPI!"}



