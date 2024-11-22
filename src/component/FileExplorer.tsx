import React, { useState } from 'react';
import { Folder, File, ArrowRight } from 'lucide-react';
import AnalysisDashboard from './AnalysisDashboard';

interface FileInfo {
  name: string;
  type: string;
  size: string;
}

export default function FileExplorer() {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const items = Array.from(e.dataTransfer.items);
    const newFiles: FileInfo[] = [];

    for (const item of items) {
      const entry = item.webkitGetAsEntry();
      if (entry?.isFile) {
        const file = await new Promise<File>((resolve) => {
          entry.file((file: File) => resolve(file));
        });
        
        newFiles.push({
          name: file.name,
          type: file.type || 'unknown',
          size: formatFileSize(file.size),
        });
      }
    }

    setFiles(newFiles);
    if (newFiles.length > 0) {
      setShowAnalysis(true);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-black flex flex-col">
      <header className="pt-12 pb-16 px-4">
        <h1 className="text-5xl font-bold text-center bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight">
          repo.ai
        </h1>
      </header>

      <div className="flex-1 flex items-start justify-center px-4 pb-8">
        <div className="w-full max-w-6xl">
          {!showAnalysis ? (
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`
                w-full aspect-[2/1] max-h-[400px] rounded-xl mb-8 transition-all duration-300 backdrop-blur-sm
                flex items-center justify-center
                ${isDragging 
                  ? 'bg-green-900/30 border-2 border-green-400 shadow-[0_0_30px_rgba(74,222,128,0.3)]' 
                  : 'bg-green-900/20 border-2 border-green-500/30 hover:border-green-400/50 hover:shadow-[0_0_20px_rgba(74,222,128,0.2)]'}
              `}
            >
              <div className="flex flex-col items-center justify-center text-green-400 p-8">
                <Folder className="w-20 h-20 mb-6 animate-pulse" />
                <p className="text-xl mb-3 font-medium">Drop your folder here</p>
                <p className="text-green-500/70">Files will be analyzed instantly</p>
              </div>
            </div>
          ) : (
            <AnalysisDashboard 
              files={files} 
              onBack={() => setShowAnalysis(false)} 
            />
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