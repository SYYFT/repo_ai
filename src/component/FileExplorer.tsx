import React, { useState } from "react";
import { Folder, UploadCloud, Github, Laugh, X, CheckCircle } from "lucide-react";
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
  const [loading, setLoading] = useState(false);
  const [isUploadPopupOpen, setIsUploadPopupOpen] = useState(false);
  const [uploadedFileCount, setUploadedFileCount] = useState(0);
  const [isRepoError, setIsRepoError] = useState(false);

  const navigate = useNavigate();

  // 📌 Process files & show confirmation popup
  const processFiles = async (fileList: File[]) => {
    const newFiles: FileInfo[] = fileList.map(file => ({
      name: file.name,
      type: file.type || "unknown",
      size: formatFileSize(file.size),
      file: file,
    }));

    setFiles(newFiles);

    if (newFiles.length > 0) {
      setUploadedFileCount(newFiles.length);
      setIsUploadPopupOpen(true); // ✅ Show upload confirmation popup
    }
  };

  // 📌 Handle file selection (Folder Upload)
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

  // 📌 Extract repo name from GitHub URL
  const getRepoName = (url: string) => {
    return url.split("/").slice(-1)[0].replace(".git", "");
  };

  // 📌 Handle Repo Link Submission
  const handleRepoSubmit = async () => {
    if (!repoLink.startsWith("https://github.com/")) {
      setIsRepoError(true); // ✅ Show popup instead of alert
      return;
    }

    setLoading(true);
    const repoName = getRepoName(repoLink);

    try {
      // Step 1: Send repo URL to FastAPI to clone
      const response = await fetch("http://localhost:8000/fetch-repo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoLink }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Failed to fetch repo");

      // Step 2: Convert API response to FileInfo[] format
      const newFiles: FileInfo[] = data.files.map((file: string) => ({
        name: file,
        type: file.split(".").pop() || "unknown",
        size: "Unknown",
      }));

      // Step 3: Store the files in state
      setFiles(newFiles);

      // Step 4: Navigate to Analysis Dashboard
      navigate("/analysis");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to process repository.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="absolute top-6 left-1/2 -translate-x-1/2 cursor-pointer" onClick={() => navigate("/")}>
        <h1 className="text-7xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight" style={{ fontFamily: "'Nova Square', sans-serif" }}>repo.ai</h1>
      </div>

      {/* 📌 -------------------------------------------------------------------------- Upload Confirmation Popup */}
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
          <Folder className="w-16 h-16" style={{ color: "#022C22" }} />
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

        {/* 📌 Upload Confirmation Popup */}
        {isUploadPopupOpen && (
          <div className="fixed inset-0 flex items-center justify-center z-50">
            {/* Backdrop */}
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setIsUploadPopupOpen(false)} />

            {/* Popup Content */}
            <div className="relative bg-gray-900 border-2 border-green-400 rounded-xl p-6 max-w-md w-full m-4 transform transition-all">
              <button 
                onClick={() => setIsUploadPopupOpen(false)}
                className="absolute top-4 right-4 text-green-400 hover:text-green-300"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex flex-col items-center gap-4">
                <CheckCircle className="w-12 h-12 text-green-400" />
                <h2 className="text-xl font-semibold text-green-400 text-center">
                  {uploadedFileCount} File{uploadedFileCount > 1 ? "s" : ""} Uploaded!
                </h2>
                <p className="text-lg text-green-400 text-center">
                  Your files are ready for analysis.
                </p>

                {/* Proceed to Analysis Button */}
                <button
                  onClick={() => navigate("/analysis")}
                  className="mt-3 px-4 py-2 bg-green-800 text-white rounded-lg hover:bg-green-600 transition"
                >
                  Go to Analysis
                </button>
              </div>
            </div>
          </div>
        )}


        {/* 📌 GitHub/Bitbucket Repository Link (Bottom Left) */}
        <div className="flex flex-col items-center justify-center bg-green-700 rounded-lg p-6 transition-all duration-300">
          <Github className="w-16 h-16" style={{ color: "#022C22" }} />
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
            disabled={loading}
          >
            {loading ? "Processing..." : "Submit"}
          </button>
        </div>

          {/* 📌 Invalid Repo Link Popup */}
          {isRepoError && (
            <div className="fixed inset-0 flex items-center justify-center z-50">
              {/* Backdrop */}
              <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setIsRepoError(false)} />

              {/* Popup Content */}
              <div className="relative bg-gray-900 border-2 border-red-500 rounded-xl p-6 max-w-md w-full m-4 transform transition-all">
                <button 
                  onClick={() => setIsRepoError(false)}
                  className="absolute top-4 right-4 text-red-400 hover:text-red-300"
                >
                  <X className="w-5 h-5" />
                </button>

                <div className="flex flex-col items-center gap-4">
                  <Github className="w-12 h-12 text-red-400" />
                  <h2 className="text-xl font-semibold text-red-400 text-center">
                    Invalid Repository URL!
                  </h2>
                  <p className="text-lg text-red-400 text-center">
                    Please enter a valid GitHub repository link.
                  </p>

                  {/* Close Button */}
                  <button
                    onClick={() => setIsRepoError(false)}
                    className="mt-3 px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-600 transition"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          )}


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

              {/* Joke Text (Without the Laugh Icon at the Top) */}
              <h2 className="text-xl font-semibold text-green-400 text-center mb-4">
                Why do programmers prefer dark mode?
              </h2>

              <p className="text-lg text-green-400 text-center">
                Because light attracts bugs!
              </p>

              {/* 📌 Move the Laugh Icon to Bottom Right */}
              <div className="absolute bottom-4 right-4">
                <Laugh className="w-6 h-6 text-green-400" />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
