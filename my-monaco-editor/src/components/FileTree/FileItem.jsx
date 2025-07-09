import React from 'react';
import { FileText } from 'lucide-react';
import { useFileStore } from '../../store/fileStore';

const FileItem = ({ file, path }) => {
  const setActiveFile = useFileStore((state) => state.setActiveFile);
  const activeFilePath = useFileStore((state) => state.activeFile.path);

  const isActive = path === activeFilePath;

  const handleClick = () => {
    setActiveFile(file.handle, path);
  };

  return (
    <div
      className={`flex items-center p-1 rounded-md hover:bg-[#37373d] cursor-pointer ${isActive ? 'bg-[#37373d]' : ''}`}
      onClick={handleClick}
    >
      <FileText size={16} className="mr-2 text-blue-400 shrink-0" />
      <span className="truncate">{file.name}</span>
    </div>
  );
};

export default FileItem;