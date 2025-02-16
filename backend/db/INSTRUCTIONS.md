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

### Branch Usage Guidelines

For effective collaboration and organized development, each branch is used based on the type of task being performed. Follow these guidelines to select the correct branch and naming convention:

1. **Data Architecture Branches**
   - **Usage**: For tasks related to database structure, stored procedures, automation, or any direct manipulation of the database.
   - **Branch Prefix**: `data-architecture-<layer>`
   - **Naming Convention**: Include the task name and your username to track work effectively. Follow the format:
     ```
     data-architecture-<layer>-/<ticket-number>-<task-name>-<username>
     ```
   - **Example**:
     ```
     data-architecture-test-/01-creating-ddl-scripts-deeahnuh
     ```

2. **Data Engineering Branches**
   - **Usage**: For tasks related to code that interacts with data sources, ingestion processes, or ETL pipelines.
   - **Branch Prefix**: `data-engineering-<layer>`
   - **Naming Convention**: Follow the same format to maintain consistency:
     ```
     data-engineering-<layer>-/<ticket-number>-<task-name>-<username>
     ```
   - **Example**:
     ```
     data-engineering-dev-/02-setup-aws-ingestion-deeahnuh
     ```

3. **Data Analytics Branches**
   - **Usage**: For tasks focused on data analysis, building visualizations, and generating insights from data.
   - **Branch Prefix**: `data-analytics-<layer>`
   - **Naming Convention**: Consistent with other branches, to clearly identify task type, ticket, and user:
     ```
     data-analytics-<layer>-/<ticket-number>-<task-name>-<username>
     ```
   - **Example**:
     ```
     data-analytics-prod-/03-create-visualizations-deeahnuh
     ```

### Summary

- **Layer Types**:
  - `dev`: For initial development and testing in a non-production environment.
  - `test`: For quality assurance and final checks before deployment.
  - `prod`: For production-ready changes that are fully tested.

- **Naming Convention**: `<branch-prefix>-<layer>-/<ticket-number>-<task-name>-<username>`

---

### DuckDB Database Structure and Schema Management

DuckDB operates slightly differently from other databases, such as PostgreSQL or MySQL. In DuckDB:

- **Single Database File**: Each `.db` file is treated as a standalone database. This means that instead of having multiple databases (e.g., `DEV`, `TEST`, `PROD`), DuckDB uses separate files for each environment.
  - Example: For a development environment, the database file might be `repo_ai_dev.db`, while the test environment could use `repo_ai_test.db`.

- **Schemas as Logical Namespaces**: Within each database file, **schemas** act as logical namespaces. This allows you to organize tables and other database objects logically without creating separate databases within the same file.
  - Schemas like `ingestion`, `processing`, `analytics`, and `sandbox` can be used across different files for consistent structure.

- **No `USE DATABASE` Command**: Since each `.db` file is self-contained, DuckDB doesn’t support a `USE DATABASE` command. Instead, you specify which database file to connect to by providing the file path when connecting.

### How to Check Schemas in DuckDB

To view all schemas within a DuckDB database file:

1. **Connect to the Database**:
   - Open the database file by specifying its path. In DuckDB’s shell, for example:
     ```sql
     .open /path/to/repo_ai_dev.db
     ```

2. **List Schemas**:
   - Use the following query to list all schemas within the database file:
     ```sql
     SELECT schema_name FROM information_schema.schemata;
     ```

This approach allows you to maintain separate database files for DEV, TEST, and PROD environments, each containing the same schema structure (e.g., `ingestion`, `processing`, `analytics`, `sandbox`) for consistency across environments.

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
