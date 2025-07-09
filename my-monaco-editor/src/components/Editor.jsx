import React from 'react';
import { Editor as MonacoEditor } from '@monaco-editor/react';
import { useFileStore } from '../store/fileStore';

const Editor = () => {
  const { activeFile, updateActiveFileContent } = useFileStore((state) => ({
    activeFile: state.activeFile,
    updateActiveFileContent: state.updateActiveFileContent,
  }));

  const handleEditorChange = (value) => {
    updateActiveFileContent(value);
  };

  // This wrapper div is crucial for capturing the context menu event
  // before it reaches the Monaco Editor's default handler.
  return (
    <div className="flex-1 overflow-hidden" onContextMenu={(e) => e.preventDefault()}>
      {activeFile.handle ? (
        <MonacoEditor
          height="100%"
          path={activeFile.path}
          value={activeFile.content}
          onChange={handleEditorChange}
          theme="vs-dark"
          options={{
            fontSize: 14,
            minimap: { enabled: true },
            contextmenu: false, // Disables the editor's default context menu
            wordWrap: 'on',
          }}
        />
      ) : (
        <div className="flex items-center justify-center h-full text-gray-500">
          <p>Select a file to begin editing.</p>
        </div>
      )}
    </div>
  );
};

export default Editor;