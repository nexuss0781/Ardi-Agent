import React, { useState } from 'react';

const FileTreeItem = ({ item, level, onFileClick, onFolderClick, onExpandToggle }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
    if (item.kind === 'directory') {
      onExpandToggle(item.handle, !isExpanded);
    }
  };

  const handleClick = () => {
    if (item.kind === 'file') {
      onFileClick(item.handle, item.path);
    } else {
      onFolderClick(item.handle, item.path);
      handleToggle(); // Toggle expand/collapse on folder click
    }
  };

  const indentation = level * 15; // 15px per level

  return (
    <div style={{ paddingLeft: `${indentation}px`, whiteSpace: 'nowrap' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          cursor: 'pointer',
          padding: '4px 0',
          '&:hover': { backgroundColor: '#333' },
        }}
        onClick={handleClick}
      >
        {item.kind === 'directory' ? (
          <span onClick={(e) => { e.stopPropagation(); handleToggle(); }} style={{ marginRight: '5px' }}>
            {isExpanded ? '▼' : '▶'}
          </span>
        ) : (
          <span style={{ width: '15px', display: 'inline-block', marginRight: '5px' }}></span> // Spacer for files
        )}
        <span style={{ marginRight: '5px' }}>{item.kind === 'directory' ? '📁' : '📄'}</span>
        <span>{item.name}</span>
      </div>
      {isExpanded && item.children && (
        <div style={{ marginLeft: '10px' }}>
          {item.children.map((child) => (
            <FileTreeItem
              key={child.path}
              item={child}
              level={level + 1}
              onFileClick={onFileClick}
              onFolderClick={onFolderClick}
              onExpandToggle={onExpandToggle}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default FileTreeItem;
