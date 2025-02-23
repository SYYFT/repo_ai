import logging
import csv
import unicodedata
from datetime import datetime


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("wikipedia_cleanup")

def load_file_formats(file_path):
    """
    Loads file formats from a CSV file.
    """
    logger.info(f"Loading file formats from {file_path}")
    file_formats = []
    
    with open(file_path, mode="r", encoding="utf-8", errors="replace") as file:
        reader = csv.DictReader(file)
        for row in reader:
            file_formats.append(row)
    
    return file_formats

def clean_file_formats(file_formats):
    """
    Cleans the file_formats list of dictionaries by replacing the en dash '–' with a comma
    and moving the second portion to 'description'.
    """
    logger.info("Cleaning file formats data")

    for entry in file_formats:
        if "extension" in entry and isinstance(entry["extension"], str):
            # Normalize encoding to avoid unexpected characters
            normalized_extension = unicodedata.normalize("NFKD", entry["extension"])
            
            # Replace en dash (U+2013) with a comma + space for readability
            normalized_extension = normalized_extension.replace("–", ", ")
            
            # Split the extension into two parts if applicable
            parts = normalized_extension.split(", ", 1)  
            entry["extension"] = parts[0].strip()
            
            # Append second part to description if it exists
            if len(parts) > 1:
                entry["description"] = parts[1].strip() + " " + entry.get("description", "").strip()
                entry["description"] = entry["description"].strip()

    logger.info("File formats data cleaned successfully")
    return file_formats

def check_unexpected_characters(file_formats):
    """Checks if any extensions or descriptions still contain unexpected characters."""
    unexpected_chars = ["–", "â€“", "  "]  # Double spaces indicate cleaning issues
    issues = []

    for i, entry in enumerate(file_formats):
        for char in unexpected_chars:
            if char in entry["extension"]:
                issues.append((i, "extension", entry["extension"]))
            if char in entry["description"]:
                issues.append((i, "description", entry["description"]))

    if issues:
        logger.warning(f"Found {len(issues)} unexpected character issues.")
        for issue in issues[:5]:  
            logger.warning(f"Row {issue[0]} | Column: {issue[1]} | Value: {issue[2]}")
    else:
        logger.info("No unexpected character issues found.")
    
    return issues

def check_missing_fields(file_formats):
    """Checks if there are any missing values in required fields."""
    issues = []

    for i, entry in enumerate(file_formats):
        for field in ["category", "extension", "description", "notes"]:
            if entry[field] == "" or entry[field] is None:
                issues.append((i, field, entry[field]))

    if issues:
        logger.warning(f"Found {len(issues)} missing values.")
        for issue in issues[:5]:
            logger.warning(f"Row {issue[0]} | Column: {issue[1]} is missing")
    else:
        logger.info("No missing value issues found.")
    
    return issues

def check_duplicate_extensions(file_formats):
    """Identifies duplicate extensions in the data."""
    seen = {}
    duplicates = []

    for i, entry in enumerate(file_formats):
        ext = entry["extension"].lower()
        if ext in seen:
            duplicates.append((i, ext))
        else:
            seen[ext] = i

    if duplicates:
        logger.warning(f"Found {len(duplicates)} duplicate extensions.")
        for duplicate in duplicates[:5]:
            logger.warning(f"Row {duplicate[0]} | Duplicate Extension: {duplicate[1]}")
    else:
        logger.info("No duplicate extensions found.")
    
    return duplicates

def check_extensions_without_descriptions(file_formats):
    """Identifies extensions with no descriptions."""
    issues = []

    for i, entry in enumerate(file_formats):
        if entry["description"] == "":
            issues.append((i, entry["extension"]))

    if issues:
        logger.warning(f"Found {len(issues)} extensions without descriptions.")
        for issue in issues[:5]:
            logger.warning(f"Row {issue[0]} | Extension: {issue[1]} has no description")
    else:
        logger.info("All extensions have descriptions.")
    
    return issues

def save_file_formats(file_formats, filename="cleaned_file_formats.csv"):
    """
    Saves the cleaned file formats data to a CSV file with UTF-8 encoding,
    ensuring proper encoding of special characters.
    """
    logger.info("Saving cleaned file formats to file")
    headers = ["category", "extension", "description", "notes"]

    with open(filename, mode="w", newline="", encoding="utf-8", errors="replace") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for entry in file_formats:
            writer.writerow(entry)
    
    logger.info(f"File successfully saved as {filename}")

def main(file_path):
    """Main function to clean and quality check file format data."""
    logger.info("Starting file format cleanup process")
    
    file_formats = load_file_formats(file_path)
    file_formats = clean_file_formats(file_formats)
    
    logger.info("Running data quality checks...")
    check_unexpected_characters(file_formats)
    check_missing_fields(file_formats)
    check_duplicate_extensions(file_formats)
    check_extensions_without_descriptions(file_formats)
    
    save_file_formats(file_formats)
    
    logger.info("Process finished")

if __name__ == "__main__":


    date = datetime.now().strftime('%m%d%y')
    file_path = f"C:\\Users\\dvalladares\\Repos\\repo_ai\\backend\\processed\\file_formats_{date}.csv" 
    main(file_path)
