import React from 'react';
import { useFileStore } from '../../store/fileStore';
import FolderItem from './FolderItem';
import FileItem from './FileItem';

const FileTree = () => {
  const fileTree = useFileStore((state) => state.fileTree);

  // Sort entries so folders appear before files
  const sortedEntries = Object.values(fileTree).sort((a, b) => {
    if (a.kind === b.kind) return a.name.localeCompare(b.name);
    return a.kind === 'directory' ? -1 : 1;
  });

  return (
    <div className="flex-1 p-2 overflow-y-auto">
      {sortedEntries.map(entry => (
        entry.kind === 'directory' ? (
          <FolderItem key={entry.name} folder={entry} path={entry.name} />
        ) : (
          <FileItem key={entry.name} file={entry} path={entry.name} />
        )
      ))}
    </div>
  );
};

export default FileTree;