# SYYFT's Repo.ai

A tool to help developers understand codebases through visualization and natural language queries.

## Features
- Visualize code dependencies and relationships
- Query the codebase using natural language
- Interactive UI with infinity scrolling
- Built on DuckDB for efficient data storage

## Quick Start Guide 🚀

### Starting the App

#### On Mac/Linux:
```bash
./start_codespace_app.sh
```

#### On Windows:
Using Git Bash:
```bash
bash start_codespace_app.sh
```

Using CMD:
```cmd
start_codespace_app.bat
```

The app will start two services:
- Backend (FastAPI): `http://127.0.0.1:8000`
- Frontend (Vite): `http://localhost:5173`

### Using the App
1. Open the frontend URL in your browser
2. Enter a GitHub repository link
3. Wait for the repository to be fetched and parsed
4. Explore the codebase visualization!

## Troubleshooting

If the backend isn't running:
```bash
curl -X GET "http://127.0.0.1:8000/"
```
If that fails, restart it with:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload --reload-exclude cloned_repos
```

If the frontend isn't loading:
```bash
npm run dev
```

If nothing works, run the startup script again:
```bash
./start_codespace_app.sh
```

## Tech Stack
- Backend: FastAPI, Python, DuckDB
- Frontend: TypeScript, React
- Visualization: D3.js/Cytoscape.js

## License
MIT License


### Updated Folder Structure:
```
repo_ai/                        # Root directory of your project
│── docs/                        # API Documentation
│   ├── api_endpoints.md         # API endpoint details
│   ├── api_overview.md          # Overview of the API
│   ├── index.md                 # Documentation index
│
│── src/                         # React/TypeScript Frontend
│   ├── components/              # React Components
│   │   ├── AnalysisDashboard.tsx # Dashboard component
│   │   ├── FileExplorer.tsx      # File Explorer component
│   │   ├── WelcomePage.tsx       # Landing Page component
│   ├── fonts/                    # Fonts used in the frontend
│   ├── App.tsx                   # Main App component
│   ├── main.tsx                  # Application entry point
│   ├── vite.env.d.ts             # TypeScript environment types
│
│── backend/                      # FastAPI Backend
│   ├── server.py                 # API Server
│   ├── main.py                   # Backend entry point
│   ├── parser/                    # Parsing-related scripts
│   │   ├── parser.py              # Parses repositories
│   ├── db/                        # Database structure
│   │   ├── dev/                   # Development database
│   │   ├── test/                  # Test database
│   │   ├── prod/                  # Production database
│
│── parsed_repo.json               # JSON output file (if not using API)
│── package.json                   # Frontend package configuration
│── README.md                      # Project documentation
│── .env                            # Environment variables (set by start_codespace.sh)
│── start_codespace.sh              # Script to set VITE_API_URL in `.env`
│── .gitignore                      # Git ignore rules
│── eslint.config.js                # ESLint configuration
│── LICENSE                         # Project license
│── mkdocs.yml                      # MkDocs configuration for documentation
│── package-lock.json               # Lockfile for package dependencies
│── tailwind.config.js              # Tailwind CSS configuration
│── tsconfig.app.json               # TypeScript config for the app
│── tsconfig.json                   # TypeScript base config
│── tsconfig.node.json              # TypeScript config for Node.js
│── vite.config.ts                   # Vite configuration

```
