import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from datetime import datetime

# Base URL
BASE_URL = "https://fileinfo.com/filetypes/"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# File storage path
SAVE_DIR = r"C:\Users\dvalladares\Repos\repo_ai\backend\raw"
os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure directory exists

# Generate filename timestamp
timestamp = datetime.now().strftime("%m%d%y")


def get_file_info_cat():
    """
    Scrapes file extensions and descriptions from FileInfo.com by category,
    including popularity score, and saves them to a timestamped CSV file.
    """
    categories = [
        "common", "text", "audio", "video", "compressed", "spreadsheet", "ebook", "executable",
        "raster_image", "camera_raw", "vector_image", "3d_image",
        "page_layout", "developer", "database", "game", "web", "cad", "gis",
        "plugin", "font", "system", "settings", "encoded", "disk_image",
        "backup", "data", "misc"
    ]

    csv_filename = os.path.join(SAVE_DIR, f"files_info_{timestamp}_category.csv")
    file_formats = []

    for category in categories:
        url = f"{BASE_URL}{category}"
        print(f"Scraping: {url}")

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) > 2:
                file_extension = cols[0].get_text(strip=True)
                file_description = cols[1].get_text(strip=True)
                popularity = cols[2].find("span", class_="hidden")

                popularity_score = popularity.get_text(strip=True) if popularity else "N/A"

                file_formats.append([file_extension, file_description, category, popularity_score])

        time.sleep(2)  # Prevent rate limiting

    # Save results
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Extension", "Description", "Category", "Popularity"])
        writer.writerows(file_formats)

    print(f"File format dictionary (category-based) saved as {csv_filename}")


def get_files_info_alph():
    """
    Scrapes file extensions and descriptions from FileInfo.com by alphabet
    (A-Z, plus '1' for numerical file extensions), including popularity score,
    and saves to a CSV.
    """
    alphabets = ["1"] + [chr(i) for i in range(ord('a'), ord('z') + 1)]  # ['1', 'a', 'b', ..., 'z']

    csv_filename = os.path.join(SAVE_DIR, f"files_info_{timestamp}_alphabet.csv")
    file_formats = []

    for letter in alphabets:
        url = f"{BASE_URL}{letter}"
        print(f"Scraping: {url}")

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) > 2:
                file_extension = cols[0].get_text(strip=True)
                file_description = cols[1].get_text(strip=True)
                popularity = cols[2].find("span", class_="hidden")

                popularity_score = popularity.get_text(strip=True) if popularity else "N/A"

                file_formats.append([file_extension, file_description, letter.upper(), popularity_score])

        time.sleep(2)  # Prevent rate limiting

    # Save results
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Extension", "Description", "Alphabet", "Popularity"])
        writer.writerows(file_formats)

    print(f"File format dictionary (alphabet-based) saved as {csv_filename}")


# Example usage
if __name__ == "__main__":
    get_file_info_cat()   # Scrape file types by category
    get_files_info_alph() # Scrape file types by alphabet
