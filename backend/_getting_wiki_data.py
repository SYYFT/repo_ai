import requests
import json
import csv
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import unicodedata
import re
import os 


# Setup logging
current_date = datetime.now().strftime('%m%d%y')
log_filename = f"C:\\Users\\dvalladares\\Repos\\repo_ai\\backend\\raw\\file_format_parser_wikipedia_{current_date}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()



# Regex pattern: Initial period, all uppercase, 2-15 characters, no spaces
VALID_EXTENSION_REGEX = r"^\.[A-Z]{2,15}$"


def fetch_and_prettify_soup():
    """
    Fetch the Wikipedia page and return a prettified BeautifulSoup object
    """
    try:
        url = "https://en.wikipedia.org/wiki/List_of_file_formats"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content div
        content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            logger.error("Could not find main content div")
            return None
            
        # Prettify the content
        pretty_html = content.prettify()
        
        # Create new soup from prettified HTML
        pretty_soup = BeautifulSoup(pretty_html, 'html.parser')
        
        logger.info("Successfully fetched and prettified Wikipedia content")
        return pretty_soup
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Wikipedia page: {e}")
        return None
    except Exception as e:
        logger.error(f"Error processing HTML content: {e}")
        return None

def parse_file_formats(soup):
    """
    Parse file formats from Wikipedia page content.
    Handles both cases where headings have spans and where they don't.
    """
    file_formats = []
    current_category = ""
    
    # Find all headings and lists in the content
    content = soup.find_all(['h2', 'h3', 'ul'])
    
    for element in content:
        if element.name in ['h2', 'h3']:
            # Try first with span
            heading_span = element.find('span', {'class': 'mw-headline'})
            if heading_span:
                current_category = heading_span.get_text(strip=True)
            else:
                # If no span, get text directly from heading
                current_category = element.get_text(strip=True)
            
            logger.info(f"Found category: {current_category}")
                
        elif element.name == 'ul' and current_category:
            for li in element.find_all('li', recursive=False):
                try:
                    # Get the full text content
                    full_text = li.get_text(strip=True)
                    logger.debug(f"Processing item under {current_category}: {full_text[:50]}...")
                    
                    # Extract extension and description
                    parts = full_text.split(' – ', 1)  # Try en dash first
                    if len(parts) < 2:
                        parts = full_text.split(' - ', 1)  # Try regular hyphen
                    
                    if len(parts) >= 2:
                        extensions = parts[0].strip()
                        description = parts[1].strip()
                    else:
                        extensions = parts[0].strip()
                        description = ""
                    
                    # Split multiple extensions (comma-separated)
                    extension_list = [ext.strip() for ext in extensions.split(',')]
                    
                    # Extract notes from links
                    notes = []
                    for a in li.find_all('a'):
                        if a.get('href') and a.get('title'):
                            notes.append(f"{a.get_text()} ({a['title']})")
                    
                    # Add each extension as a separate entry
                    for ext in extension_list:
                        ext = ext.strip('.').strip()
                        if ext:
                            entry = {
                                'category': current_category,
                                'extension': ext,
                                'description': description,
                                'notes': '; '.join(notes) if notes else ''
                            }
                            file_formats.append(entry)
                            logger.debug(f"Added entry: {entry}")
                            
                except Exception as e:
                    logger.error(f"Error processing list item: {e}")
                    continue
    
    return file_formats

def save_file_formats(file_formats, output_file):
    """
    Saves cleaned file formats data to a CSV file, ensuring that only expected fields are written.

    Args:
        file_formats (list of dict): List of file format dictionaries.
        output_file (str): Path to save the CSV file.
    """
    if not file_formats:
        print("No data to save.")
        return

    # Get the set of all possible fields (handle missing fields gracefully)
    fieldnames = set()
    for entry in file_formats:
        fieldnames.update(entry.keys())  # Ensure all potential keys are included

    # Ensure consistent field order
    ordered_fields = ["extension", "description", "category"]
    if "popularity" in fieldnames:
        ordered_fields.append("popularity")  # Only add popularity if it exists

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_fields)
        writer.writeheader()
        for entry in file_formats:
            # Only write fields that exist in fieldnames
            filtered_entry = {k: v for k, v in entry.items() if k in ordered_fields}
            writer.writerow(filtered_entry)

    print(f"File saved successfully: {output_file}")

def clean_file_formats(file_formats):
    """
    Cleans the file_formats list by:
    - Replacing en dash '–' with a comma
    - Ensuring extensions start with a period (.)
    - Converting extensions to uppercase
    - Removing entries with spaces in the extension
    - Filtering extensions that don't match the regex pattern
    - Moving invalid extensions to a 'dirty_data' list
    - Trimming spaces from all columns
    
    Args:
        file_formats (list of dict): List containing dictionaries with "extension" and "description".
        
    Returns:
        tuple: (cleaned_file_formats, dirty_data)
    """
    logger.info("Cleaning file formats data")

    cleaned_file_formats = []
    dirty_data = []

    for entry in file_formats:
        if "extension" in entry and isinstance(entry["extension"], str):
            # Normalize encoding to avoid unexpected characters
            normalized_extension = unicodedata.normalize("NFKD", entry["extension"]).strip()

            # Replace en dash (U+2013) with a comma + space
            normalized_extension = normalized_extension.replace("–", ", ")

            # Split extension into parts if applicable (e.g., "ABC – Another Format" → "ABC" + description)
            parts = normalized_extension.split(", ", 1)
            normalized_extension = parts[0].strip()  # Keep first part as the extension

            # Append second part to description if it exists
            if len(parts) > 1:
                entry["description"] = parts[1].strip() + " " + entry.get("description", "").strip()

            # Trim all fields
            entry["description"] = entry.get("description", "").strip()
            entry["category"] = entry.get("category", "").strip()  # If category exists, trim it
            entry["popularity"] = entry.get("popularity", "").strip()  # If popularity exists, trim it

            # Convert to uppercase and prepend a period if missing
            if not normalized_extension.startswith("."):
                normalized_extension = "." + normalized_extension
            normalized_extension = normalized_extension.upper()

            # Remove if extension has spaces or doesn't match the regex
            if " " in normalized_extension or not re.match(VALID_EXTENSION_REGEX, normalized_extension):
                dirty_data.append(entry)  # Move invalid entries to dirty data list
                continue

            # Update the cleaned entry
            entry["extension"] = normalized_extension
            cleaned_file_formats.append(entry)

    logger.info(f"Cleaning complete: {len(cleaned_file_formats)} valid entries, {len(dirty_data)} dirty entries")

    return cleaned_file_formats, dirty_data

def main():
    """
    Main function to orchestrate the file format parsing process
    """
    try:
        logger.info("Starting file format parsing process")
        
        # Fetch and prettify content
        pretty_soup = fetch_and_prettify_soup()
        if not pretty_soup:
            logger.error("Failed to fetch and prettify content")
            return
            
        # Debug: Print first few headings to verify structure
        logger.debug("First few headings found:")
        for heading in pretty_soup.find_all(['h2', 'h3'])[:3]:
            logger.debug(heading.prettify())
        
        # Parse file formats
        logger.info("Beginning to parse file formats")
        file_formats = parse_file_formats(pretty_soup)

        # Clean file formats
        clean_file_formats_data, dirty_data = clean_file_formats(file_formats)
        
        # Check if we got any results
        if not file_formats:
            logger.warning("No file formats were parsed")
            return
        
        # Generate output filename with timestamp
        output_file = f"C:\\Users\\dvalladares\\Repos\\repo_ai\\backend\\raw\\wikipedia_{current_date}.csv"
        processed_file = f"C:\\Users\\dvalladares\\Repos\\repo_ai\\backend\\processed\\wikipedia_{current_date}.csv"
        
        # Save results to CSV
        save_file_formats(file_formats, output_file)
        save_file_formats(clean_file_formats_data, processed_file)

        #dirty data 
        save_file_formats(dirty_data, output_file)
        
        # Log summary statistics
        logger.info(f"Processing complete. Found {len(file_formats)} file formats")
        
        # Print category summary
        categories = set(fmt['category'] for fmt in file_formats)
        logger.info(f"Categories found: {len(categories)}")
        for category in sorted(categories):
            count = sum(1 for fmt in file_formats if fmt['category'] == category)
            logger.info(f"  {category}: {count} formats")
            
        # Debug: Print sample of parsed formats
        logger.debug("Sample of parsed formats:")
        for fmt in file_formats[:5]:
            logger.debug(fmt)
            
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")
        raise
    
    finally:
        logger.info("Process finished")


if __name__ == "__main__":
    try:
        # Add debug logging for development
        logger.setLevel(logging.DEBUG)
        
        # Add console handler for immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise

