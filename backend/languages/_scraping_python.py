import requests
from bs4 import BeautifulSoup
import chromadb
from tqdm import tqdm

# 🛠️ Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_reusable_code")
collection = client.get_or_create_collection("reusable_code_docs")

# 🌎 Documentation URLs for Each Language
DOC_URLS = {
    "Python": "https://docs.python.org/3/tutorial/modules.html",
    "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules",
    "Java": "https://docs.oracle.com/javase/tutorial/java/package/index.html",
    "C++": "https://en.cppreference.com/w/cpp/header",
    "C#": "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/namespaces/",
    "Go": "https://go.dev/ref/mod",
    "Rust": "https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html",
    "PHP": "https://www.php.net/manual/en/function.require.php",
    "Swift": "https://developer.apple.com/library/archive/documentation/Swift/Conceptual/Swift_Programming_Language/Modules.html",
    "Bash": "https://www.gnu.org/software/bash/manual/bash.html#Functions",
    "SQL": "https://www.postgresql.org/docs/current/sql.html"
}

# 📥 Function to Scrape Documentation Page
def scrape_doc(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    structured_data = []
    current_section = "General"

    for tag in soup.find_all():
        if tag.name in ["h1", "h2", "h3"]:  # Section titles
            current_section = tag.get_text(strip=True)
        elif tag.name == "p":  # Paragraphs
            structured_data.append((current_section, tag.get_text(strip=True)))

    return structured_data

# 🔄 Scrape & Store Data in ChromaDB
print(f"📚 Scraping and structuring reusable code documentation...")

for idx, (language, url) in tqdm(enumerate(DOC_URLS.items()), total=len(DOC_URLS), desc="Scraping Docs"):
    doc_data = scrape_doc(url)
    
    for i, (sub_section, content) in enumerate(doc_data):
        collection.add(
            ids=[f"{idx}-{i}"],
            documents=[content],
            metadatas=[{"language": language, "section": sub_section, "source": url}]
        )

print("\n🚀 Reusable code documentation successfully structured and stored in ChromaDB!")
