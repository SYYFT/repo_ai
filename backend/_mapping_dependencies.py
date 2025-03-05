import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load language patterns CSV
language_patterns = pd.read_csv("backend/raw/language_patterns.csv")

# Ensure `file_defined` and `file_used` columns are filled correctly
language_patterns = language_patterns.dropna(subset=["file_used", "reference_type"])  # Remove incomplete rows

# Dictionary to track where modules/functions are defined
definition_map = {}

# First pass: Identify definitions
for _, row in language_patterns.iterrows():
    if row["reference_type"] == "Function Definition" and pd.notna(row["file_defined"]):
        definition_map[row["module_name"]] = row["file_defined"]

# Second pass: Map function calls & imports to their definitions
edges = []
for _, row in language_patterns.iterrows():
    file_used = row["file_used"]
    module_name = row["module_name"]
    reference_type = row["reference_type"]

    # If it's an import or function call, check if we know where it was defined
    if reference_type in ["Import", "Function Call"] and module_name in definition_map:
        file_defined = definition_map[module_name]
        if file_defined != file_used:  # Avoid self-references
            edges.append((file_defined, file_used, reference_type, module_name))

# Create directed graph
G = nx.DiGraph()

# Add edges to the graph
for file_defined, file_used, reference_type, module_name in edges:
    G.add_edge(file_defined, file_used, label=f"{reference_type}: {module_name}")

# Check if graph has nodes
if len(G.nodes) == 0:
    print("⚠️ No relationships found after enrichment! Check your CSV file.")

# Plot the graph
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)  # Improved layout for better spacing
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=8, edge_color="gray")
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Updated File Dependency Graph (Python Repository)")
plt.show()
