import os
import ast
from neo4j import GraphDatabase

class RepoParser:
    def __init__(self, repo_path, neo4j_uri, neo4j_user, neo4j_password):
        self.repo_path = repo_path
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def parse_repository(self):
        """ Loop through all Python files in the repo and parse them. """
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.parse_file(file_path)

    def parse_file(self, file_path):
        """ Parse functions, imports, and dependencies in a file. """
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        file_node = {"path": file_path.replace(self.repo_path, "").strip("/\\")}
        functions = []
        imports = []
        dependencies = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):  
                functions.append(node.name)  # Store function names

            elif isinstance(node, ast.Import):  
                for alias in node.names:
                    imports.append(alias.name)  # Store standard imports

            elif isinstance(node, ast.ImportFrom):  
                imports.append(node.module)  # Store relative imports

            elif isinstance(node, ast.Call):  
                if isinstance(node.func, ast.Attribute):
                    dependencies.append(node.func.value.id)  # Store called functions
                elif isinstance(node.func, ast.Name):
                    dependencies.append(node.func.id)

        self.store_in_neo4j(file_node, functions, imports, dependencies)

    def store_in_neo4j(self, file, functions, imports, dependencies):
        """ Store extracted data in Neo4j """
        with self.driver.session() as session:
            session.write_transaction(self._store_file, file)
            for func in functions:
                session.write_transaction(self._store_function, file, func)
            for imp in imports:
                session.write_transaction(self._store_import, file, imp)
            for dep in dependencies:
                session.write_transaction(self._store_dependency, file, dep)

    @staticmethod
    def _store_file(tx, file):
        """ Create File node in Neo4j """
        tx.run("MERGE (f:File {path: $path})", path=file["path"])

    @staticmethod
    def _store_function(tx, file, function_name):
        """ Create Function node and link to File """
        tx.run("""
            MERGE (fn:Function {name: $function_name})
            MERGE (fn)-[:DEFINED_IN]->(f:File {path: $file_path})
        """, function_name=function_name, file_path=file["path"])

    @staticmethod
    def _store_import(tx, file, import_name):
        """ Create IMPORTS relationship between a File and an imported module """
        tx.run("""
            MERGE (imp:Library {name: $import_name})
            MERGE (imp)-[:IMPORTED_IN]->(f:File {path: $file_path})
        """, import_name=import_name, file_path=file["path"])

    @staticmethod
    def _store_dependency(tx, file, dependency):
        """ Create DEPENDS_ON relationship between files """
        tx.run("""
            MERGE (dep:File {path: $dependency})
            MERGE (f:File {path: $file_path})
            MERGE (f)-[:DEPENDS_ON]->(dep)
        """, dependency=dependency, file_path=file["path"])

    def close(self):
        self.driver.close()

# Example Usage
repo_path = "backend/cloned_repos/repo_ai"
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "password"

parser = RepoParser(repo_path, neo4j_uri, neo4j_user, neo4j_password)
parser.parse_repository()
parser.close()
