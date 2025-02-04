import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FileExplorer from "./component/FileExplorer";
import AnalysisDashboard from "./component/AnalysisDashboard";

interface FileInfo {
  name: string;
  type: string;
  size: string;
  file?: File;
}

function App() {
  const [files, setFiles] = useState<FileInfo[]>([]);

  return (
    <Router>
      <div className="min-h-screen bg-black flex flex-col">
        {/* Header */}
        <header className="pt-12 pb-16 px-4">
          <h1 
            className="text-5xl font-bold text-center bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight" 
            style={{ fontFamily: "'Nova Square', sans-serif" }}
          >
            repo.ai
          </h1>
        </header>

        {/* Routes for File Upload and Analysis */}
        <main className="flex-1 flex items-start justify-center px-4 pb-8">
          <div className="w-full max-w-6xl">
            <Routes>
              <Route path="/" element={<FileExplorer setFiles={setFiles} />} />
              <Route path="/analysis" element={<AnalysisDashboard files={files} onBack={() => window.history.back()} />} />
            </Routes>
          </div>
        </main>

        {/* Footer */}
        <footer className="p-4 text-center">
          <a
            href="https://syyft.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block text-green-400 hover:text-green-300 transition-colors duration-300 group"
          >
            <span className="relative">
              syyft.com
              <div className="h-px w-0 group-hover:w-full absolute bottom-0 left-0 bg-gradient-to-r from-green-400 to-emerald-500 transition-all duration-300" />
            </span>
          </a>
        </footer>
      </div>
    </Router>
  );
}

export default App;
