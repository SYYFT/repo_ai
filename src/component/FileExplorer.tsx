import React, { useState } from "react";
import { Folder, UploadCloud, Github, Laugh, X } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface FileInfo {
  name: string;
  type: string;
  size: string;
  file?: File;
}

interface FileExplorerProps {
  setFiles: (files: FileInfo[]) => void;
}

export default function FileExplorer({ setFiles }: FileExplorerProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [repoLink, setRepoLink] = useState("");
  const [isJokeOpen, setIsJokeOpen] = useState(false);
  const navigate = useNavigate();

  // 📌 Process files & navigate to analysis
  const processFiles = async (fileList: File[]) => {
    const newFiles: FileInfo[] = fileList.map(file => ({
      name: file.name,
      type: file.type || "unknown",
      size: formatFileSize(file.size),
      file: file,
    }));
    
    setFiles(newFiles);
    if (newFiles.length > 0) {
      navigate("/analysis");
    }
  };

  // 📌 Handle file selection (input field)
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      processFiles(Array.from(e.target.files));
    }
  };

  // 📌 Handle Drag & Drop, supporting folders
  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    processFiles(Array.from(e.dataTransfer.files));
  };

  // 📌 Convert bytes to readable format
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  // 📌 Handle Repo Link Submission
  const handleRepoSubmit = () => {
    if (repoLink.trim() !== "") {
      console.log("Repository Link Submitted:", repoLink);
      alert("Repository link submitted!"); // Optional confirmation message
    }
  };

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="absolute top-6 left-1/2 -translate-x-1/2 cursor-pointer" onClick={() => navigate("/")}>
        <h1 className="text-7xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight" style={{ fontFamily: "'Nova Square', sans-serif" }}>repo.ai</h1>
      </div>
      <div className="grid grid-cols-2 grid-rows-2 gap-4 w-3/4 h-3/4">
        {/* 📌 Drop Folder or Files (Top Left) */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`flex flex-col items-center justify-center border-2 border-green-400 rounded-lg p-6 transition-all duration-300 backdrop-blur-sm cursor-pointer ${
            isDragging ? "bg-green-900/40 shadow-lg" : "bg-green-900/20"
          }`}
        >
          <Folder className="w-16 h-16 text-green-400 mb-3" />
          <p className="text-lg font-medium text-green-400">Drop Folder or Files Here</p>
        </div>

        {/* 📌 Select Folder or Files (Top Right) */}
        <div className="flex flex-col items-center justify-center bg-green-700 rounded-lg p-6 transition-all duration-300">
          <input
            type="file"
            multiple
            // @ts-ignore
            webkitdirectory="" 
            directory=""
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer text-white font-medium px-6 py-3 rounded-lg bg-green-800 hover:bg-green-600 transition"
          >
            Select Folder or Files
          </label>
        </div>

        {/* 📌 GitHub/Bitbucket Repository Link (Bottom Left) */}
        <div className="flex flex-col items-center justify-center bg-green-700 rounded-lg p-6 transition-all duration-300">
          <Github className="w-16 h-16 text-white mb-3" />
          <p className="text-lg font-medium text-white mb-2">GitHub/Bitbucket Repository Link</p>
          <input
            type="text"
            value={repoLink}
            onChange={(e) => setRepoLink(e.target.value)}
            placeholder="Paste your repo link here..."
            className="w-3/4 p-2 rounded-md bg-gray-900 text-white border border-gray-600 focus:border-green-400 focus:outline-none"
          />
          <button
            onClick={handleRepoSubmit}
            className="mt-3 px-4 py-2 bg-green-800 text-white rounded-lg hover:bg-green-600 transition"
          >
            Submit
          </button>
        </div>

        {/* 📌 Tell Me a Joke (Bottom Right) */}
        <div
          onClick={() => setIsJokeOpen(true)}
          className="flex flex-col items-center justify-center border-2 border-green-400 rounded-lg p-6 transition-all duration-300 cursor-pointer bg-green-900/20 hover:bg-green-900/40"
        >
          <Laugh className="w-16 h-16 text-green-400 mb-3" />
          <p className="text-lg font-medium text-green-400">Tell me a joke</p>
        </div>

        {/* Custom Joke Dialog */}
        {isJokeOpen && (
          <div className="fixed inset-0 flex items-center justify-center z-50">
            {/* Backdrop */}
            <div 
              className="absolute inset-0 bg-black/50 backdrop-blur-sm"
              onClick={() => setIsJokeOpen(false)}
            />
            
            {/* Dialog Content */}
            <div className="relative bg-gray-900 border-2 border-green-400 rounded-xl p-6 max-w-md w-full m-4 transform transition-all">
              <button 
                onClick={() => setIsJokeOpen(false)}
                className="absolute top-4 right-4 text-green-400 hover:text-green-300"
              >
                <X className="w-5 h-5" />
              </button>
              
              <div className="flex items-center gap-2 mb-4">
                <Laugh className="w-6 h-6 text-green-400" />
                <h2 className="text-xl font-semibold text-green-400">Here's your joke!</h2>
              </div>
              
              <p className="text-lg text-green-400 text-center">
                Why do programmers prefer dark mode? Because light attracts bugs!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}