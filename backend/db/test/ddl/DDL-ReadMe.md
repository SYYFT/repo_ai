# 📂 DDL (Data Definition Language)

## Overview
The **DDL** folder contains SQL scripts for defining and managing the database structure. DDL commands are used to create, modify, and delete database objects like tables, schemas, and indexes. These scripts help establish the structure of the database without affecting the data itself.

## Key Operations
- **CREATE**: Defines new database objects, such as tables and schemas.
- **ALTER**: Modifies the structure of existing objects, such as adding or removing columns from a table.
- **DROP**: Deletes entire database objects, removing them from the database.
- **TRUNCATE**: Removes all data from a table quickly, without logging individual deletions.

## Folder Contents
- Scripts for creating tables, schemas, indexes, and other database structures.
- Modifications to existing database objects to accommodate new requirements.

## Usage
Run the scripts in this folder to set up or modify the database structure. Be cautious with `DROP` and `TRUNCATE` commands, as they can permanently delete objects or data.


# 📊 Database Schema: Language Import Rules & Patterns

## **1️⃣ Table: `language_import_rules`**
This table defines **static import rules** for each programming language.

| Column Name      | Data Type | Description |
|-----------------|-----------|-------------|
| `id`           | SERIAL PRIMARY KEY | Unique identifier for the rule |
| `language`     | TEXT NOT NULL | Programming language (Python, JavaScript, etc.) |
| `pattern`      | TEXT NOT NULL | Example of how imports look in that language |
| `reference_type` | TEXT NOT NULL | Describes the type of import (e.g., "ES6 Module Import", "Python Standard Import") |

### **📌 Example Data**
| id | language   | pattern                             | reference_type |
|----|-----------|-------------------------------------|----------------|
| 1  | HTML      | `<script src="app.js"></script>`    | JavaScript Import |
| 2  | JavaScript | `import x from './module.js'`      | ES6 Module Import |
| 3  | Python    | `import module_name`               | Python Standard Import |
| 4  | C++       | `#include "file.hpp"`              | Header File |

---

## **2️⃣ Table: `language_patterns`**
This table stores **actual imports detected in real repositories**, dynamically linked to `language_import_rules`.

| Column Name      | Data Type | Description |
|-----------------|-----------|-------------|
| `id`           | SERIAL PRIMARY KEY | Unique identifier for detected import |
| `language`     | TEXT NOT NULL | Programming language detected |
| `module_name`  | TEXT NOT NULL | Name of the imported module (e.g., `express`, `numpy`) |
| `file_defined` | TEXT NOT NULL | File where the module is **defined** |
| `file_used`    | TEXT NOT NULL | File where the module is **used** |
| `reference_type` | TEXT NOT NULL | Type of import (matches `language_import_rules.reference_type`) |
| `import_rule_id` | INT | Foreign Key referencing `language_import_rules.id` |

### **📌 Example Data**
| id | language   | module_name | file_defined    | file_used      | reference_type        | import_rule_id |
|----|-----------|-------------|----------------|---------------|----------------------|---------------|
| 1  | JavaScript | `express`   | `server.js`   | `app.js`      | ES6 Module Import   | 2 |
| 2  | Python    | `os`        | `utils.py`    | `main.py`     | Python Standard Import | 3 |
| 3  | C++       | `iostream`  | `main.cpp`    | `main.cpp`    | Standard Library Import | 4 |

---

## **🔗 How These Tables Are Connected**
The **`language_patterns.import_rule_id`** column **links** to **`language_import_rules.id`**, ensuring that each detected import is mapped to a predefined pattern.

### **🔀 Relationship Diagram**
```plaintext
+------------------------+      +-------------------------+       +----------------------+
| language_import_rules  |      | language_patterns       |       | parsed_files         |
|------------------------|      |-------------------------|       |----------------------|
| id (PK)               |◄─────| import_rule_id (FK)     |       | id (PK)              |
| language              |      | language                |       | file_path            |
| pattern               |      | module_name             |       | repo_name            |
| regex                 |      | file_defined (FK)       |◄─────| file_path (FK)       |
| reference_type        |      | file_used (FK)          |       | upload_source        |
+------------------------+      | reference_type          |       | processed_at         |
                                +-------------------------+       +----------------------+
