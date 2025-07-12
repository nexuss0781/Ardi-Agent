import React from 'react';
import Editor from '@monaco-editor/react';

// This component wraps the Monaco Editor to provide a clean interface for our app.

interface EditorProps {
  code: string;
  language: string;
}

const CodeEditor: React.FC<EditorProps> = ({ code, language }) => {
  return (
    <div className="editor-container">
      <Editor
        height="100%"
        width="100%"
        language={language}
        value={code}
        theme="vs-dark" // A standard dark theme
        options={{
          selectOnLineNumbers: true,
          minimap: { enabled: true },
          fontSize: 14,
          scrollBeyondLastLine: false,
        }}
      />
    </div>
  );
};

export default CodeEditor;