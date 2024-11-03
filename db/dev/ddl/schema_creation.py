import duckdb

#---------------------------------- 
#-------- CONNECT TO DUCDB --------
#---------------------------------- 
conn = duckdb.connect('db/dev/repo_ai_dev.db')

#---------------------------------- 
#-------- CREATE SCHEMAS IN DEV ---
#---------------------------------- 
conn.execute("CREATE SCHEMA IF NOT EXISTS ingestion;")
conn.execute("CREATE SCHEMA IF NOT EXISTS processing;")
conn.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
conn.execute("CREATE SCHEMA IF NOT EXISTS sandbox;")

#---------------------------------- 
#-------- QC  ---------------------
#---------------------------------- 
schemas = conn.execute("SELECT schema_name FROM information_schema.schemata;").fetchall()
print("Schemas created:", schemas)

conn.close()
