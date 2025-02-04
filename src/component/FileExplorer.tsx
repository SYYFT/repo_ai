import React, { useState } from "react";
import { Folder, UploadCloud } from "lucide-react";
import AnalysisDashboard from "./AnalysisDashboard";

interface FileInfo {
  name: string;
  type: string;
  size: string;
  file?: File;
}

export default function FileExplorer() {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [showSummary, setShowSummary] = useState(false);

  const processFiles = async (fileList: FileList) => {
    const newFiles: FileInfo[] = [];
    for (const file of Array.from(fileList)) {
      newFiles.push({
        name: file.name,
        type: file.type || "unknown",
        size: formatFileSize(file.size),
        file: file,
      });
    }
    setFiles(newFiles);
    if (newFiles.length > 0) setShowSummary(true);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      processFiles(e.target.files);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files) {
      processFiles(e.dataTransfer.files);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className="min-h-screen bg-black flex flex-col">
    <header className="pt-12 pb-16 px-4">
      <h1 
        className="text-5xl font-bold text-center bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight" 
        style={{ fontFamily: "'Nova Square', sans-serif" }} // Apply font only here
      >
        repo.ai
      </h1>
    </header>
      <div className="flex-1 flex items-start justify-center px-4 pb-8">
        <div className="w-full max-w-6xl">
          {!showSummary ? (
            <>
              {/* Drag & Drop Box */}
              <div
                onDragOver={(e) => {
                  e.preventDefault();
                  setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                className={`
                  w-full aspect-[2/1] max-h-[400px] rounded-xl mb-8 transition-all duration-300 backdrop-blur-sm
                  flex items-center justify-center
                  ${
                    isDragging
                      ? "bg-green-900/30 border-2 border-green-400 shadow-[0_0_30px_rgba(74,222,128,0.3)]"
                      : "bg-green-900/20 border-2 border-green-500/30 hover:border-green-400/50 hover:shadow-[0_0_20px_rgba(74,222,128,0.2)]"
                  }
                `}
              >
                <div className="flex flex-col items-center justify-center text-green-400 p-8">
                  <Folder className="w-20 h-20 mb-6 animate-pulse" />
                  <p className="text-xl mb-3 font-medium">Drop your folder or files here</p>
                  <p className="text-green-500/70">Files will be analyzed instantly</p>
                </div>
              </div>

              {/* File Select */}
              <div className="flex flex-col items-center">
                <input
                  type="file"
                  multiple
                  webkitdirectory="true"
                  directory="true"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer bg-green-700 px-6 py-2 rounded-md text-white font-medium hover:bg-green-600 transition"
                >
                  Select Folder or Files
                </label>
              </div>
            </>
          ) : (
            <AnalysisDashboard files={files} />
          )}
        </div>
      </div>

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
  );
}
