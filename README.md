# 📊 Repository Insights App

#### URL: https://chatgpt.com/share/672ab8c4-d4e0-8010-9e77-34f72d1195ef
## Overview
The **Repository Insights App** is designed to help new team members quickly understand the structure and functionality of a codebase. By uploading a repository folder or providing a GitHub link, this app visualizes code dependencies, function calls, and module imports, allowing developers to explore code relationships through an interactive UI. The app also includes an integrated language model that can answer questions about the repository, such as _"How many times is `getAWSCredits` used in this repo?"_

## Features
- **Dependency Mapping**: Visualizes connections between files and functions, showing where imports and function calls occur across the codebase.
- **Natural Language Queries**: Users can ask questions about the repository (e.g., function usage frequency, file dependencies) and receive insights directly from a chatbot.
- **Infinity Scrolling UI**: Seamless exploration of files and functions with dynamic loading as the user navigates.
- **Backend with DuckDB**: Efficient storage and querying of repository metadata. Future migration planned to **Polars** for optimized data processing.

## Tech Stack
| Component           | Technology                        |
|---------------------|-----------------------------------|
| **Backend**         | DuckDB for data storage          |
|                     | Python for data parsing          |
|                     | Polars for high-performance processing (planned) |
| **Frontend**        | JavaScript (D3.js or Cytoscape.js) for visualization |
|                     | Infinity Scroll for navigation   |
| **LLM Integration** | Language Model for querying insights |

## Data Structure
The backend uses DuckDB to store metadata about the repository:

- **Files Table**: Contains file paths.
- **Functions Table**: Stores function definitions and their associated files.
- **Imports Table**: Tracks import relationships between files.



---

## High-Level Architecture

### Components

1. **Backend**  
   - **Data Processing**: Python script to parse the repository, extract metadata (functions, imports, dependencies), and load it into a DuckDB database.
   - **Data Storage**: DuckDB stores information about files, functions, and imports, enabling efficient querying.
   - **API**: Serves data to the frontend for visualizations and processes LLM-based queries.

2. **Frontend**
   - **UI for Visualization**: Built with JavaScript libraries (e.g., D3.js or Cytoscape.js) to display file and function dependencies using arrow connections.
   - **Infinity Scrolling**: Dynamically loads file information as the user scrolls, minimizing load times and improving user experience.
   - **Query Interface**: Allows users to ask questions about the repository (e.g., function call counts), receiving answers from the backend.

3. **LLM Integration**
   - **Question Answering**: A language model (LLM) to interpret and respond to user queries about repository insights.
   - **Query Processing**: LLM translates questions into SQL or Polars queries for DuckDB and returns responses.

---

## Folder Structure

repo-insights-app/
├── db/                     # Database folder (DuckDB database files)
│   └── repository_data.db   # DuckDB database for repository insights
├── src/
│   ├── backend/             # Backend code and API
│   │   ├── parse_repo.py    # Script to parse repository and populate DuckDB
│   │   ├── query_api.py     # API for frontend data requests and LLM queries
│   │   └── utils/           # Utility functions for data processing
│   ├── frontend/            # Frontend code
│   │   ├── index.html       # HTML entry point
│   │   ├── app.js           # JavaScript for visualization and infinity scroll
│   │   └── styles.css       # Styling for the frontend
├── ARCHITECTURE.md          # This architecture document
├── README.md                # Project overview and setup
└── requirements.txt         # Python dependencies


## Data Flow

### Repository Parsing

- **Input**: A local folder path or GitHub link.
- **Process**: `parse_repo.py` uses Python’s `ast` module to parse code, extract function definitions, imports, and dependencies.
- **Storage**: Metadata is stored in `db/repository_data.db` in DuckDB.

### Data Visualization

- The frontend retrieves data from the backend API (`query_api.py`) and displays file and function relationships.
- Dependencies between files and function calls are visualized with arrows, allowing users to see how files interact.

### LLM Query Handling

- **User Query**: A user inputs a question in natural language.
- **Processing**: The LLM processes the question, forms an SQL or Polars query, and retrieves data from DuckDB.
- **Response**: The LLM returns a response to the frontend, displayed in the query interface.

---

## Future Enhancements

- **Polars Integration**: Migrate to Polars for high-performance data processing.
- **Expanded Query Capabilities**: Add advanced querying options for repository insights.
- **Custom Visualizations**: Provide additional visual insights into code structure and usage.

---

## Dependencies

- **DuckDB**: Lightweight database for analytical queries.
- **Python**: Backend data processing and API.
- **JavaScript (D3.js or Cytoscape.js)**: Visualization library for the frontend.
- **Polars**: *(Future)* For optimized data manipulation and analysis.

---


## Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/repo-insights-app.git
cd repo-insights-app

### 2. Set Up Virtual Enviornment

python -m venv repo-ai-v
source repo-ai-v/bin/activate  # On Windows: repo-ai-v\Scripts\activate


## Usage

- **Upload Repository**: Use the app interface to upload a repository folder or provide a GitHub link.
- **Explore Dependencies**: The app’s UI displays file and function relationships, allowing users to explore dependencies with arrowed connections
- **Ask Question**: Use the chatbot to ask questions about the repository, such as usage frequency of specific functions or import relationships.


## Future Enhancements

- Polars Integration: Migrate to Polars for faster data processing.
- Advanced LLM Integrations: Improve the chatbot’s understanding of repository structure and provide deeper insights.
- Expanded Query Capabilities: Enable specific insights on code dependencies and functionality.


## Contributing

- 1. Fork the repository.
- 2. Create a new branch (git checkout -b feature/your-feature).
- 3. Commit your changes (git commit -m 'Add new feature').
- 4. Push to the branch (git push origin feature/your-feature).
- 5. Open a Pull Request.

## License

This project is licensed under the MIT License.
