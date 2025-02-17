import os
import ast
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to parse a single Python file
def parse_file(filepath):
    """Parses a Python file to extract functions, classes, and imports."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=filepath)
    except Exception as e:
        logging.error(f"❌ Failed to parse {filepath}: {e}")
        return [], [], []

    functions, classes, imports = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for name in node.names:
                imports.append(name.name)

    return functions, classes, imports

# Function to parse a repository directory
def parse_repository(repo_path):
    """Walks through a repository directory, parses each Python file, and returns structured JSON data."""
    if not os.path.exists(repo_path):
        logging.error(f"❌ Repository path {repo_path} does not exist.")
        return {"error": "Repository path does not exist"}

    repo_data = {
        "files": [],
        "functions": {},
        "classes": {},
        "imports": {}
    }

    for root, _, files in os.walk(repo_path):
        for file_name in files:
            if file_name.endswith('.py'):
                filepath = os.path.normpath(os.path.join(root, file_name))  # Normalize paths
                
                # Parse the file
                functions, classes, imports = parse_file(filepath)

                # Store parsed data
                repo_data["files"].append(filepath)
                repo_data["functions"][filepath] = functions
                repo_data["classes"][filepath] = classes
                repo_data["imports"][filepath] = imports

    logging.info("✅ Repository parsing complete.")
    return repo_data  # ⬅️ Now returns a structured dictionary instead of a string!

# Function to save parsed data to a JSON file
def save_parsed_data(parsed_data, output_file="parsed_repo.json"):
    """Saves parsed JSON data to a file."""
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(parsed_data, json_file, indent=4)  # ✅ Use json.dump() for proper formatting
        logging.info(f"✅ Parsed data saved to {output_file}")
    except Exception as e:
        logging.error(f"❌ Failed to save parsed data: {e}")

# Example usage
if __name__ == "__main__":
    repo_path = "SAMPLE_REPO"  # Change to actual repo path
    parsed_data = parse_repository(repo_path)
    save_parsed_data(parsed_data)
