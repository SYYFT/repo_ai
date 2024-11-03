# 📐 Repository Insights App Database Architecture

## Overview
The Repository Insights App database is organized into three environments: **DEV**, **TEST**, and **PROD**. Each environment contains consistent schemas, making it easy to maintain and scale as the project grows.

### Environments

1. **DEV** – Development environment for creating and testing new stored procedures and processes.
2. **TEST** – Testing environment containing both raw and cleaned data, ideal for running validation checks and QA before promoting to production.
3. **PROD** – Production environment with only clean, processed data for stable, reliable use by end-users.

---

## Schemas and Tables

Each environment includes three schemas (`ingestion`, `processing`, and `analytics`), which support data ingestion, cleaning, processing, and analytics. This structure is scalable and adaptable as the app evolves.

### 1. `ingestion` Schema
Handles the initial raw data ingestion.

- **Tables**:
  - `raw_files` – Stores metadata about files in the repository, including paths, file types, and sizes.
  - `raw_functions` – Contains raw information about function definitions (e.g., name, location, file ID).
  - `raw_imports` – Tracks dependencies and import relationships between files.
  
### 2. `processing` Schema
For staging and processing raw data, cleaning, and preparing for analysis.

- **Tables**:
  - `cleaned_files` – Cleaned and standardized metadata about files, with invalid entries filtered out.
  - `cleaned_functions` – Parsed function definitions, verified and cleaned, ready for analysis.
  - `function_dependencies` – Processed relationships between functions, including import hierarchies and dependencies.

### 3. `analytics` Schema
Stores final, aggregated, and analyzed data that powers insights and visualizations.

- **Tables**:
  - `file_dependency_graph` – Summary of file dependencies, used for visualization.
  - `function_usage_stats` – Aggregated stats on function calls, including usage frequency and inter-file dependencies.
  - `query_logs` – Stores logs of queries processed by the LLM, for analytics and improving LLM responses.

---
### DDL and DML Folders

- **DDL (Data Definition Language)**: The `ddl/` folder contains SQL scripts for creating, altering, and deleting database structures, including schemas, tables, and indexes. These scripts are used to define and manage the database architecture. Key operations include `CREATE`, `ALTER`, and `DROP` commands, which establish the overall structure of the database across DEV, TEST, and PROD environments.

- **DML (Data Manipulation Language)**: The `dml/` folder holds SQL scripts for manipulating data within the database. These scripts include commands for inserting, updating, deleting, and querying data in existing tables. Common DML operations include `INSERT`, `UPDATE`, `DELETE`, and `SELECT`, enabling data modification and retrieval for testing, validation, and analytics.

---

## Example Database Structure

| Environment | Schema      | Table                    | Description                                                 |
|-------------|-------------|--------------------------|-------------------------------------------------------------|
| DEV         | ingestion   | raw_files                | Raw file metadata ingestion table                           |
| DEV         | ingestion   | raw_functions            | Raw function definitions and metadata                       |
| DEV         | ingestion   | raw_imports              | Initial import relationships between files                  |
| DEV         | processing  | cleaned_files            | Cleaned file metadata for further processing                |
| DEV         | processing  | cleaned_functions        | Cleaned function definitions, verified                      |
| DEV         | processing  | function_dependencies    | Parsed dependencies and function-call relationships         |
| DEV         | analytics   | file_dependency_graph    | Summary table for file dependencies                         |
| DEV         | analytics   | function_usage_stats     | Aggregated function usage statistics                        |
| DEV         | analytics   | query_logs               | Logs of LLM queries, including type and frequency           |
| TEST        | ingestion   | raw_files                | Test table for raw file metadata                            |
| TEST        | ingestion   | raw_functions            | Test table for raw function definitions                     |
| TEST        | ingestion   | raw_imports              | Test table for initial import relationships                 |
| TEST        | processing  | cleaned_files            | Test-cleaned file metadata                                  |
| TEST        | processing  | cleaned_functions        | Test-cleaned function definitions                           |
| TEST        | processing  | function_dependencies    | Test dependencies between functions                         |
| TEST        | analytics   | file_dependency_graph    | Test table for file dependency summary                      |
| TEST        | analytics   | function_usage_stats     | Test table for function usage stats                         |
| TEST        | analytics   | query_logs               | Test table for query logs                                   |
| PROD        | ingestion   | N/A                      | (No raw tables in production)                               |
| PROD        | processing  | N/A                      | (No intermediate tables in production)                      |
| PROD        | analytics   | file_dependency_graph    | Final production summary of file dependencies               |
| PROD        | analytics   | function_usage_stats     | Final production statistics on function usage               |
| PROD        | analytics   | query_logs               | Final production query logs for insight into usage patterns |

---

## Notes on Scalability

1. **Schema Consistency**: Each environment (DEV, TEST, PROD) has identical schemas (`ingestion`, `processing`, and `analytics`), ensuring consistency and straightforward migration across environments.
2. **Modularity**: Tables are logically separated by function, making it easy to add new data sources or functions as the project scales.
3. **Growth-Ready Analytics**: The `analytics` schema is designed to aggregate data, which can easily be expanded with more tables as insights grow in complexity.

---
