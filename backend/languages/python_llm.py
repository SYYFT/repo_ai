import chromadb

# 🛠️ Connect to ChromaDB
client = chromadb.PersistentClient(path="./vector_db/chroma_reusable_code")
collection = client.get_collection("reusable_code_docs")

# 🔍 Query the vector database
def query_docs(question, language=None):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    if not results["documents"]:
        return ["No results found."]

    formatted_results = []
    for i in range(len(results["documents"])):
        # 🛠️ FIX: Index into the metadata list correctly
        lang = results["metadatas"][0][i].get("language", "Unknown Language")
        section = results["metadatas"][0][i].get("section", "Unknown Section")
        text = results["documents"][0][i]

        # 🔍 Filter by language if specified
        if language and lang.lower() != language.lower():
            continue

        formatted_results.append(f"\n📌 **Language: {lang}**\n🔹 **Section: {section}**\n{text}\n")

    return formatted_results


# Example Queries
question = "How does Python handle modules?"
answers = query_docs(question, language="Python")

for answer in answers:
    print(answer)
