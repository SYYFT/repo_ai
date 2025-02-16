import os

#---------------------------------- 
#------ BASE DIRECTORY TO MIMICK --
#---------------------------------- 
base_dir = '/workspaces/repo_ai/db/dev'

#---------------------------------- 
#-------- SECTIONS IN REPO --------
#---------------------------------- 
sections = ['ddl', 'dml']
schemas = ['ingestion', 'processing', 'analytics', 'sandbox']

#---------------------------------- 
#-------- FOLDER STRUCTURE --------
#---------------------------------- 
for section in sections:
    section_dir = os.path.join(base_dir, section)
    os.makedirs(section_dir, exist_ok=True)
    
    # Create schema folders within each section (ddl and dml)
    for schema in schemas:
        schema_dir = os.path.join(section_dir, schema)
        os.makedirs(schema_dir, exist_ok=True)
        print(f"Created folder: {schema_dir}")

print("Folder structure for DEV database schemas under ddl and dml initialized successfully.")
