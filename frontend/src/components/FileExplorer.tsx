import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

interface FileExplorerProps {
  onFileSelect: (path: string, language: string) => void;
  refreshKey: number; // The key that will trigger a refresh
}

const getLanguageFromExtension = (filename: string): string => {
  const extension = filename.split('.').pop()?.toLowerCase() || '';
  switch (extension) {
    case 'py': return 'python'; case 'js': return 'javascript';
    case 'ts': return 'typescript'; case 'tsx': return 'typescript';
    case 'css': return 'css'; case 'html': return 'html';
    case 'json': return 'json'; case 'md': return 'markdown';
    case 'yaml': return 'yaml'; case 'dockerfile': return 'dockerfile';
    default: return 'plaintext';
  }
};

const FileExplorer: React.FC<FileExplorerProps> = ({ onFileSelect, refreshKey }) => {
  const [files, setFiles] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/workspace/files`);
        setFiles(response.data.files || []);
        setError(null); // Clear previous errors on successful fetch
      } catch (err) {
        console.error("Error fetching file list:", err);
        setError("Could not fetch workspace files.");
      }
    };
    fetchFiles();
  }, [refreshKey]); // This effect now re-runs whenever refreshKey changes


  const handleFileClick = async (filePath: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/workspace/file`, {
            params: { path: filePath }
        });
        const language = getLanguageFromExtension(filePath);
        onFileSelect(response.data.content, language);
    } catch (err) {
        console.error(`Error fetching file content for ${filePath}:`, err);
        setError(`Could not fetch content for ${filePath}.`);
    }
  };

  return (
    <div className="file-explorer">
      <h4>Workspace</h4>
      {error && <div className="error">{error}</div>}
      <ul>
        {files.length > 0 ? (
          files.map((file, index) => (
            <li key={index} onClick={() => handleFileClick(file)}>
              📄 {file}
            </li>
          ))
        ) : (
          <li>(Workspace is empty)</li>
        )}
      </ul>
    </div>
  );
};

export default FileExplorer;