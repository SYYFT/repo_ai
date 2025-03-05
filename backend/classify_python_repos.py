import pandas as pd
import re
import os
from collections import defaultdict

# Define output paths
LANGUAGE_IMPORT_RULES_CSV = "backend/raw/language_import_rules.csv"
LANGUAGE_PATTERNS_CSV = "backend/raw/language_patterns.csv"

def classify_import_patterns(parsed_csv_path):
    """Reads parsed CSV and generates dynamic import rules & regex based on observed behaviors."""
    
    # Read parsed CSV
    df = pd.read_csv(parsed_csv_path)

    # Filter only import statements
    df_imports = df[df["Type"] == "Import"]

    # Dictionary to store unique import patterns
    import_patterns = defaultdict(set)

    # Process each import statement
    for _, row in df_imports.iterrows():
        module_name = row["Module"]
        file_path = row["File"]

        # Skip invalid or empty values
        if not isinstance(module_name, str) or module_name.strip() == "":
            continue

        # Classify based on structure
        if re.match(r"^[a-zA-Z0-9_]+$", module_name):
            pattern_type = "Standard Import"
            regex_pattern = r"^import (\w+)"
        
        elif re.match(r"^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$", module_name):
            pattern_type = "Selective Import"
            regex_pattern = r"^from (\w+) import (\w+)"
        
        elif re.match(r"^[a-zA-Z0-9_]+ as [a-zA-Z0-9_]+$", module_name):
            pattern_type = "Aliased Import"
            regex_pattern = r"^import (\w+) as (\w+)"
        
        else:
            pattern_type = "Unknown Pattern"
            regex_pattern = "N/A"

        # Store unique patterns
        import_patterns[(pattern_type, regex_pattern)].add(module_name)

    # Convert to DataFrame
    import_rules_list = [
        {"language": "Python", "pattern": pattern, "regex": regex, "reference_type": ref_type}
        for (ref_type, regex), modules in import_patterns.items()
        for pattern in modules
    ]

    df_rules = pd.DataFrame(import_rules_list)

    # Save to CSV
    df_rules.to_csv(LANGUAGE_IMPORT_RULES_CSV, index=False)
    print(f"✅ Generated import rules and saved to {LANGUAGE_IMPORT_RULES_CSV}")

def process_language_patterns(parsed_csv_path):
    """Processes the parsed CSV to create a structured dataset for language patterns."""
    
    df = pd.read_csv(parsed_csv_path)
    language_patterns = []

    for _, row in df.iterrows():
        record_type = row["Type"]
        module_name = row["Module"] if pd.notna(row["Module"]) else ""
        function_name = row["Function"] if pd.notna(row["Function"]) else ""
        file_path = row["File"]

        reference_type = None

        if record_type == "Import":
            reference_type = "Import"
        elif record_type == "Definition":
            reference_type = "Function Definition"
        elif record_type == "Call":
            reference_type = "Function Call"

        # Append processed data
        language_patterns.append([
            "Python",
            module_name,
            file_path if reference_type == "Function Definition" else "",
            file_path if reference_type in ["Function Call", "Import"] else "",
            reference_type
        ])

    # Convert to DataFrame
    df_patterns = pd.DataFrame(language_patterns, columns=[
        "language", "module_name", "file_defined", "file_used", "reference_type"
    ])

    # Save to CSV
    df_patterns.to_csv(LANGUAGE_PATTERNS_CSV, index=False)
    print(f"✅ Saved language patterns dataset: {LANGUAGE_PATTERNS_CSV}")

# Example Usage
if __name__ == "__main__":
    parsed_csv_path = "backend/raw/github_Python_030425_repoai_extract.csv"  # Change to actual parsed file
    
    # Generate Import Rules
    classify_import_patterns(parsed_csv_path)

    # Generate Language Patterns
    process_language_patterns(parsed_csv_path)
