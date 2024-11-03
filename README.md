# 📊 Repository Insights App

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