import duckdb

# Define the existing DuckDB database path
DB_PATH = r"C:\Users\dvalladares\Repos\repo_ai\backend\db\database.duckdb"

def setup_test_db():
    """
    Initializes the 'test' schema and creates the 'file_formats' table in the DuckDB database.
    """
    con = duckdb.connect(DB_PATH)

    # Create the 'test' schema if it doesn't exist
    con.execute("CREATE SCHEMA IF NOT EXISTS test;")

    # Create the 'file_formats' table inside 'test' schema
    query = """
    CREATE TABLE IF NOT EXISTS test.file_formats (
        extension TEXT PRIMARY KEY,
        description TEXT,
        category TEXT,
        popularity FLOAT
    );
    """
    con.execute(query)

    con.close()
    print(f"'test' schema and table 'test.file_formats' created successfully in {DB_PATH}")

# Run the setup when executed
if __name__ == "__main__":
    setup_test_db()
