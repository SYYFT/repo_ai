import os

# Define the base directory for the DEV environment
base_dir = '/workspaces/repo_ai/db/dev'

# Define the folders for ddl and dml, and the schemas within each
sections = ['ddl', 'dml']
schemas = ['ingestion', 'processing', 'analytics', 'sandbox']

# Create the folder structure
for section in sections:
    section_dir = os.path.join(base_dir, section)
    os.makedirs(section_dir, exist_ok=True)
    
    # Create schema folders within each section (ddl and dml)
    for schema in schemas:
        schema_dir = os.path.join(section_dir, schema)
        os.makedirs(schema_dir, exist_ok=True)
        print(f"Created folder: {schema_dir}")

print("Folder structure for DEV database schemas under ddl and dml initialized successfully.")
