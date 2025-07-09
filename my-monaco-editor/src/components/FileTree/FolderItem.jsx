import React, { useState } from 'react';
import { Folder, FolderOpen, ChevronRight, ChevronDown } from 'lucide-react';
import FileItem from './FileItem';

const FolderItem = ({ folder, path }) => {
  const [isOpen, setIsOpen] = useState(false);

  const sortedChildren = Object.values(folder.children).sort((a, b) => {
    if (a.kind === b.kind) return a.name.localeCompare(b.name);
    return a.kind === 'directory' ? -1 : 1;
  });

  return (
    <div>
      <div 
        className="flex items-center p-1 rounded-md hover:bg-[#37373d] cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <ChevronDown size={16} className="mr-1 shrink-0" /> : <ChevronRight size={16} className="mr-1 shrink-0" />}
        {isOpen ? <FolderOpen size={16} className="mr-2 text-yellow-500 shrink-0" /> : <Folder size={16} className="mr-2 text-yellow-500 shrink-0" />}
        <span className="truncate">{folder.name}</span>
      </div>
      {isOpen && (
        <div className="pl-4">
          {sortedChildren.map(entry => (
            entry.kind === 'directory' ? (
              <FolderItem key={entry.name} folder={entry} path={`${path}/${entry.name}`} />
            ) : (
              <FileItem key={entry.name} file={entry} path={`${path}/${entry.name}`} />
            )
          ))}
        </div>
      )}
    </div>
  );
};

export default FolderItem;