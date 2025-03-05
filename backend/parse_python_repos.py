from datetime import datetime
import os
import ast
import csv
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GitHubRepoParser:
    """A class to clone and parse a GitHub repository or a local folder for Python function imports, definitions, and calls."""

    def __init__(self, source: str, clone_dir: str = "cloned_repos"):
        self.source = source  # Can be a GitHub URL or local folder
        self.clone_dir = Path(clone_dir)
        self.is_cloned_repo = source.startswith("https")  # Automatically determine mode
        self.repo_name = source.split("/")[-1].replace(".git", "") if self.is_cloned_repo else Path(source).name
        self.local_repo_path = self.clone_dir / self.repo_name if self.is_cloned_repo else Path(source)
        self.results = []  # Stores parsed data

    def clone_repo(self):
        """Clones a GitHub repository to a local directory if it's a remote repo."""
        if self.is_cloned_repo:
            if self.local_repo_path.exists():
                logging.info(f"✅ Repository {self.repo_name} already exists. Skipping clone.")
            else:
                logging.info(f"📥 Cloning repository: {self.source}")
                subprocess.run(["git", "clone", self.source, str(self.local_repo_path)], check=True)
                logging.info(f"✅ Repository cloned at {self.local_repo_path}")

    def parse_python_files(self):
        """Walks through the repo or folder, finds Python files, and parses them."""
        logging.info("🔍 Scanning for Python files...")
        for file_path in self.local_repo_path.rglob("*.py"):
            logging.info(f"📄 Parsing: {file_path}")
            self._parse_file(file_path)

    def _parse_file(self, file_path: Path):
        """Parses a Python file to extract imports, function definitions, and function calls."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read(), filename=str(file_path))
        except Exception as e:
            logging.error(f"❌ Error parsing {file_path}: {e}")
            return
        
        imports, functions, calls = self._extract_ast_data(tree)

        # Store results in structured format
        for imp in imports:
            self.results.append(["Import", imp["module"], imp["alias"], "", str(file_path)])

        for func in functions:
            self.results.append(["Definition", "", "", func, str(file_path)])

        for call in calls:
            self.results.append(["Call", "", "", call, str(file_path)])

    def _extract_ast_data(self, tree: ast.AST) -> Tuple[List[Dict], List[str], List[str]]:
        """Extracts imports, function definitions, and function calls from the AST."""
        imports = []
        functions = []
        calls = []

        for node in ast.walk(tree):
            # Detect Imports
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({"module": name.name, "alias": name.asname})

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module if node.module else ""
                for name in node.names:
                    imports.append({"module": module_name, "alias": name.name})

            # Detect Function Definitions
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            # Detect Function Calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                calls.append(node.func.id)

        return imports, functions, calls

    def save_results_to_csv(self):
        """Saves parsed data to a dynamically named CSV file based on source type."""
        
        # Generate timestamp (MMDDYY format)
        timestamp = datetime.now().strftime("%m%d%y")

        if self.is_cloned_repo:
            # Save as: github_repositoryName_MMDDYY_repoai_extract.csv
            output_file = f"backend/raw/github_{self.repo_name}_{timestamp}_repoai_extract.csv"
        else:
            # Save as: folder_upload_folderName_MMDDYY_repoai_extract.csv
            output_file = f"backend/raw/folder_upload_{self.repo_name}_{timestamp}_repoai_extract.csv"

        # Save CSV
        output_path = Path(output_file)
        logging.info(f"💾 Saving results to {output_path}...")

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Module", "Alias", "Function", "File"])
            writer.writerows(self.results)

        logging.info(f"✅ Data successfully saved to {output_path}")

    def run(self):
        """Executes the full pipeline: Clone (if needed), Parse, Save."""
        self.clone_repo()  # Will only clone if it's a GitHub URL
        self.parse_python_files()
        self.save_results_to_csv()


# Example Usage
if __name__ == "__main__":
    # 🚀 Example 1: Cloning a GitHub Repo (auto-detected)
    parser = GitHubRepoParser("https://github.com/TheAlgorithms/Python")
    parser.run()

    # # 🚀 Example 2: Parsing an Uploaded Folder (auto-detected)
    # parser = GitHubRepoParser("user_uploaded_code")  # This is a local folder
    # parser.run()
