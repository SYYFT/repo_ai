import duckdb

# Define the database file path
db_path = r"C:\Users\dvalladares\Repos\repo_ai\backend\db\database.duckdb"

# Connect to the DuckDB database
conn = duckdb.connect(db_path)

# Create a test table
conn.execute("""
    CREATE TABLE IF NOT EXISTS test_table (
        id INTEGER PRIMARY KEY,
        name STRING,
        age INTEGER
    );
""")

# Insert test data
conn.execute("""
    INSERT INTO test_table (id, name, age) VALUES
    (1, 'Alice', 30),
    (2, 'Bob', 25),
    (3, 'Charlie', 35);
""")

# Verify the data by selecting all rows
result = conn.execute("SELECT * FROM test_table;").fetchall()

# Close the connection
conn.close()

# Display the test data
result
