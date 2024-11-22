import React from 'react';
import { BarChart3, FileText, FolderTree, Clock, ArrowLeft, ExternalLink, Download } from 'lucide-react';

interface FileInfo {
  name: string;
  type: string;
  size: string;
}

interface AnalysisDashboardProps {
  files: FileInfo[];
  onBack: () => void;
}

export default function AnalysisDashboard({ files, onBack }: AnalysisDashboardProps) {
  const getFileTypeCount = () => {
    const types: Record<string, number> = {};
    files.forEach(file => {
      const type = file.type === 'unknown' ? 'Other' : file.type.split('/')[1]?.toUpperCase() || 'Other';
      types[type] = (types[type] || 0) + 1;
    });
    return types;
  };

  const fileTypes = getFileTypeCount();

  return (
    <div className="w-full animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={onBack}
          className="flex items-center text-green-400 hover:text-green-300 transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Upload
        </button>
        <div className="flex gap-4">
          <button className="flex items-center px-4 py-2 bg-green-900/30 text-green-400 rounded-lg hover:bg-green-900/50 transition-all border border-green-900">
            <Download className="w-4 h-4 mr-2" />
            Export Analysis
          </button>
          <button className="flex items-center px-4 py-2 bg-green-500/20 text-green-400 rounded-lg hover:bg-green-500/30 transition-all border border-green-500/30">
            <ExternalLink className="w-4 h-4 mr-2" />
            Open in Editor
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-green-500/10 rounded-lg mr-4">
              <FileText className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-green-500/70">Total Files</p>
              <p className="text-2xl font-bold text-green-400">{files.length}</p>
            </div>
          </div>
          <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-green-400 to-emerald-500" style={{ width: '100%' }} />
          </div>
        </div>

        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-green-500/10 rounded-lg mr-4">
              <FolderTree className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-green-500/70">File Types</p>
              <p className="text-2xl font-bold text-green-400">{Object.keys(fileTypes).length}</p>
            </div>
          </div>
          <div className="flex gap-1">
            {Object.keys(fileTypes).map((type, index) => (
              <div
                key={type}
                className="h-1 rounded-full"
                style={{
                  width: `${(fileTypes[type] / files.length) * 100}%`,
                  background: `rgba(74, 222, 128, ${0.3 + (index * 0.2)})`
                }}
              />
            ))}
          </div>
        </div>

        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-green-500/10 rounded-lg mr-4">
              <Clock className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-green-500/70">Last Updated</p>
              <p className="text-2xl font-bold text-green-400">Just now</p>
            </div>
          </div>
          <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-green-400 to-emerald-500 animate-pulse" style={{ width: '60%' }} />
          </div>
        </div>
      </div>

      {/* File Type Distribution */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800 mb-8">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-green-400 flex items-center">
            <BarChart3 className="w-5 h-5 mr-2" />
            File Type Distribution
          </h3>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(fileTypes).map(([type, count], index) => (
            <div
              key={type}
              className="bg-gray-900/50 p-4 rounded-lg border border-gray-800"
            >
              <div className="flex justify-between items-center mb-2">
                <span className="text-green-400 font-medium">{type}</span>
                <span className="text-green-500/70 text-sm">{count} files</span>
              </div>
              <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-400 to-emerald-500"
                  style={{ width: `${(count / files.length) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* File List */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <h3 className="text-lg font-semibold text-green-400 mb-6">File Details</h3>
        <div className="space-y-4">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center p-4 rounded-lg bg-gray-900/30 border border-gray-800 hover:border-green-900/50 transition-all"
            >
              <div className="flex-1">
                <p className="font-medium text-green-400">{file.name}</p>
                <p className="text-sm text-green-500/70">
                  {file.type === 'unknown' ? 'File' : file.type.split('/')[1]?.toUpperCase()} • {file.size}
                </p>
              </div>
              <button className="p-2 hover:bg-green-500/10 rounded-lg transition-colors">
                <Download className="w-4 h-4 text-green-400" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}