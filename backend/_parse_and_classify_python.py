import os
import ast
import csv
import subprocess
import logging
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GitHubRepoParser:
    """Clones and parses a GitHub repository or a local folder for Python function imports, definitions, calls, and class definitions."""

    def __init__(self, source: str, clone_dir: str = "cloned_repos"):
        self.source = source  
        self.clone_dir = Path(clone_dir)
        self.is_cloned_repo = source.startswith("http") and source.endswith(".git")  
        self.repo_name = source.rstrip("/").split("/")[-1].replace(".git", "") if self.is_cloned_repo else Path(source).name
        self.local_repo_path = self.clone_dir / self.repo_name if self.is_cloned_repo else Path(source).resolve()
        self.results = []  
        self.imported_modules = {}  # Store module imports
        self.defined_functions = {}  # Store function definitions
        self.defined_classes = {}  # Store class definitions

    def clone_repo(self):
        """Clones a GitHub repository to a local directory if it's a remote repo."""
        if self.is_cloned_repo:
            if self.local_repo_path.exists():
                logging.info(f"✅ Repository {self.repo_name} already exists. Skipping clone.")
            else:
                logging.info(f"📥 Cloning repository: {self.source}")
                try:
                    subprocess.run(["git", "clone", self.source, str(self.local_repo_path)], check=True)
                    logging.info(f"✅ Repository cloned at {self.local_repo_path}")
                except subprocess.CalledProcessError:
                    logging.error(f"❌ Failed to clone repository: {self.source}")

    def _extract_ast_data(self, tree: ast.AST, file_path: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
        """Extracts imports, function definitions, function calls, and class definitions from the AST."""
        
        imports, function_defs, function_calls, class_defs, class_calls = [], [], [], [], []
        
        for node in ast.walk(tree):
            # Detect Imports
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({
                        "type": "Import",
                        "module": name.name,
                        "function": "",
                        "file_defined": "",
                        "file_used": file_path
                    })
                    self.imported_modules[name.name] = name.name

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module if node.module else ""
                for name in node.names:
                    imports.append({
                        "type": "Import",
                        "module": module_name,
                        "function": name.name,
                        "file_defined": "",
                        "file_used": file_path
                    })
                    self.imported_modules[name.name] = module_name

            # Detect Function Definitions
            elif isinstance(node, ast.FunctionDef):
                function_defs.append({
                    "type": "Definition",
                    "module": file_path,
                    "function": node.name,
                    "file_defined": file_path,
                    "file_used": ""
                })
                self.defined_functions[node.name] = file_path

            # Detect Class Definitions
            elif isinstance(node, ast.ClassDef):
                class_defs.append({
                    "type": "Class Definition",
                    "module": file_path,
                    "function": node.name,
                    "file_defined": file_path,
                    "file_used": ""
                })
                self.defined_classes[node.name] = file_path

            # Detect Function Calls
            elif isinstance(node, ast.Call):
                module_name = None
                function_name = None

                if isinstance(node.func, ast.Name):  # Calls like `sin()`, `custom_func()`
                    function_name = node.func.id
                    module_name = self.imported_modules.get(function_name, None)

                elif isinstance(node.func, ast.Attribute):  # Calls like `math.cos()`
                    if isinstance(node.func.value, ast.Name):
                        module_name = self.imported_modules.get(node.func.value.id, node.func.value.id)
                        function_name = node.func.attr

                if function_name:
                    function_calls.append({
                        "type": "Call",
                        "module": module_name,
                        "function": function_name,
                        "file_defined": "",
                        "file_used": file_path
                    })

            # Detect Class Calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in self.defined_classes:  
                    class_calls.append({
                        "type": "Class Call",
                        "module": self.defined_classes[node.func.id],
                        "function": f"{node.func.id} (init)",
                        "file_defined": self.defined_classes[node.func.id],
                        "file_used": file_path
                    })

        return imports, function_defs, function_calls, class_defs, class_calls

    def _parse_file(self, file_path: Path):
        """Parses a Python file and extracts relevant AST elements."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read(), filename=str(file_path))
        except Exception as e:
            logging.error(f"❌ Error parsing {file_path}: {e}")
            return
        
        imports, function_defs, function_calls, class_defs, class_calls = self._extract_ast_data(tree, str(file_path))

        # Store all results
        self.results.extend(imports + function_defs + function_calls + class_defs + class_calls)

    def save_results_to_csv(self) -> str:
        """Saves parsed data to a dynamically named CSV file."""
        timestamp = datetime.now().strftime("%m%d%y")
        output_file = f"backend/raw/github_{self.repo_name}_{timestamp}_repoai_extract.csv"
        output_path = Path(output_file)

        logging.info(f"💾 Saving results to {output_path}...")

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["type", "module", "function", "file_defined", "file_used"])
            writer.writeheader()
            writer.writerows(self.results)

        logging.info(f"✅ Data saved to {output_path}")
        return output_file
    
    def run(self) -> str:
        """Executes the full pipeline: Clone (if needed), Parse, Save, and return CSV path."""
        try:
            self.clone_repo()  

            if not self.local_repo_path.exists():
                logging.error(f"❌ Repository path {self.local_repo_path} does not exist.")
                return None

            logging.info("🔍 Scanning for Python files...")
            for file_path in self.local_repo_path.rglob("*.py"):  
                logging.info(f"📄 Parsing: {file_path}")
                self._parse_file(file_path)  

            if not self.results:
                logging.warning("⚠️ No results found. Skipping CSV save.")
                return None

            return self.save_results_to_csv()

        except Exception as e:
            logging.error(f"❌ Error during pipeline execution: {e}")
            return None


# Run pipeline
if __name__ == "__main__":
    parser = GitHubRepoParser("https://github.com/TheAlgorithms/Python.git")
    parsed_csv = parser.run()

    if parsed_csv:
        df = pd.read_csv(parsed_csv)
        df_patterns = df[df["type"].isin(["Call", "Definition", "Class Definition", "Class Call"])]
        output_file = "backend/raw/language_patterns.csv"
        df_patterns.to_csv(output_file, index=False)
        logging.info(f"✅ Language patterns saved to {output_file}")
