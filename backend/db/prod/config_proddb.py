import duckdb

# Define the existing DuckDB database path
DB_PATH = r"C:\Users\dvalladares\Repos\repo_ai\backend\db\database.duckdb"

def setup_prod_db():
    """
    Initializes the 'prod' schema and creates the 'file_formats' table in the DuckDB database.
    """
    con = duckdb.connect(DB_PATH)

    # Create the 'prod' schema if it doesn't exist
    con.execute("CREATE SCHEMA IF NOT EXISTS prod;")

    # Create the 'file_formats' table inside 'prod' schema
    query = """
    CREATE TABLE IF NOT EXISTS prod.file_formats (
        extension TEXT PRIMARY KEY,
        description TEXT,
        category TEXT,
        popularity FLOAT
    );
    """
    con.execute(query)

    con.close()
    print(f"'prod' schema and table 'prod.file_formats' created successfully in {DB_PATH}")

# Run the setup when executed
if __name__ == "__main__":
    setup_prod_db()
