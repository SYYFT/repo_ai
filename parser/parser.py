import os
import ast
import json

# Function to parse a single Python file
def parse_file(filepath):
    """Parses a Python file to extract functions, classes, and imports."""
    with open(filepath, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filepath)

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for name in node.names:
                imports.append(name.name)

    return functions, classes, imports

# Function to parse an entire repository directory and return JSON
def parse_repository(repo_path):
    """Walks through a repository directory, parses each Python file, and returns JSON data."""
    repo_data = {
        "files": [],
        "functions": {},
        "classes": {},
        "imports": {}
    }

    for root, _, files in os.walk(repo_path):
        for file_name in files:
            if file_name.endswith('.py'):
                filepath = os.path.join(root, file_name)
                
                # Parse the file
                functions, classes, imports = parse_file(filepath)

                # Store data in the repo_data structure
                repo_data["files"].append(filepath)
                repo_data["functions"][filepath] = functions
                repo_data["classes"][filepath] = classes
                repo_data["imports"][filepath] = imports

    # Convert repo_data to JSON format
    json_data = json.dumps(repo_data, indent=4)
    return json_data

# Example usage
if __name__ == "__main__":
    repo_path = 'SAMPLE_REPO'
    parsed_json = parse_repository(repo_path)
    
    # Print or save the JSON
    print("Repository parsing complete.")
    print(parsed_json)
    
    # Optional: Save JSON to file
    with open("parsed_repo.json", "w") as json_file:
        json_file.write(parsed_json)
