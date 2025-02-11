from fastapi import FastAPI
import json
import os

import sys
import os

# Ensure the `parser/` directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "parser")))

# Now import parser.py
import parser

app = FastAPI()

# Root route to avoid 404 errors
@app.get("/")
def root():
    return {"message": "Welcome to the Repo Parser API!"}

# Endpoint to parse a repository and return JSON data
@app.get("/parse/{repo_path}")
def parse_repository_api(repo_path: str):
    """Trigger parsing of a repository and return parsed JSON."""
    if not os.path.exists(repo_path):
        return {"error": f"Repository path '{repo_path}' does not exist."}

    parsed_json = parser.parse_repository(repo_path)
    
    # Save the parsed data
    with open("parsed_repo.json", "w") as json_file:
        json_file.write(parsed_json)

    return json.loads(parsed_json)

# Endpoint to return previously parsed data
@app.get("/get_parsed_data")
def get_parsed_data():
    """Return the latest parsed repository data from JSON file."""
    if not os.path.exists("parsed_repo.json"):
        return {"error": "No parsed data available. Run /parse/{repo_path} first."}

    with open("parsed_repo.json", "r") as f:
        return json.load(f)
