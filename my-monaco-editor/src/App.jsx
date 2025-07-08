import Editor from '@monaco-editor/react';
import React, { useRef, useState, useEffect, useCallback } from 'react';
import FileTreeItem from './components/FileTreeItem';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

function App() {
  const editorRef = useRef(null);
  const terminalRef = useRef(null);
  const wsRef = useRef(null);

  const [code, setCode] = useState('// Open a folder to start editing!');
  const [showSidebar, setShowSidebar] = useState(false);
  const [directoryHandle, setDirectoryHandle] = useState(null); // Root directory handle
  const [currentFileHandle, setCurrentFileHandle] = useState(null); // Currently open file handle
  const [currentFilePath, setCurrentFilePath] = useState(''); // Path of currently open file for display
  const [fileTree, setFileTree] = useState([]); // The nested file tree structure
  const [expandedFolders, setExpandedFolders] = useState(new Set()); // Set of paths of expanded folders

  // Initialize xterm.js terminal
  useEffect(() => {
    const term = new Terminal({
      fontFamily: 'monospace',
      fontSize: 14,
      cursorBlink: true,
      theme: {
        background: '#000',
        foreground: '#FFF',
      },
    });
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalRef.current);
    fitAddon.fit();

    // Connect to WebSocket for terminal
    wsRef.current = new WebSocket('ws://localhost:5000/socket.io/?EIO=4&transport=websocket');

    wsRef.current.onopen = () => {
      console.log('Terminal WebSocket connected');
    };

    wsRef.current.on('output', data => {
      term.write(data);
    });

    wsRef.current.onclose = () => {
      console.log('Terminal WebSocket disconnected');
    };

    wsRef.current.onerror = err => {
      console.error('Terminal WebSocket error:', err);
    };

    term.onData(data => {
      // Flask-SocketIO expects messages in a specific format, e.g., 42["input", "..."]
      wsRef.current.send('42["input","' + data + '"]');
    });

    

    window.addEventListener('resize', () => {
      fitAddon.fit();
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send('42["resize",{"cols":' + term.cols + ',"rows":' + term.rows + '}]');
      }
    });

    // Cleanup
    return () => {
      term.dispose();
      wsRef.current.close();
    };

  // Recursive function to read directory contents and build tree
  const buildFileTree = useCallback(async (handle, currentPath = '') => {
    const items = [];
    for await (const entry of handle.values()) {
      const itemPath = currentPath ? `${currentPath}/${entry.name}` : entry.name;
      if (entry.kind === 'directory') {
        items.push({
          name: entry.name,
          kind: entry.kind,
          handle: entry,
          path: itemPath,
          children: expandedFolders.has(itemPath) ? await buildFileTree(entry, itemPath) : [],
        });
      } else {
        items.push({
          name: entry.name,
          kind: entry.kind,
          handle: entry,
          path: itemPath,
        });
      }
    }
    // Sort directories first, then files, both alphabetically
    items.sort((a, b) => {
      if (a.kind === 'directory' && b.kind !== 'directory') return -1;
      if (a.kind !== 'directory' && b.kind === 'directory') return 1;
      return a.name.localeCompare(b.name);
    });
    return items;
  }, [expandedFolders]);

  // Effect to rebuild tree when directoryHandle or expandedFolders changes
  useEffect(() => {
    if (directoryHandle) {
      buildFileTree(directoryHandle).then(setFileTree);
    }
  }, [directoryHandle, expandedFolders, buildFileTree]);

  // Open a folder using File System Access API
  async function openFolder() {
    try {
      const handle = await window.showDirectoryPicker();
      setDirectoryHandle(handle);
      setExpandedFolders(new Set()); // Reset expanded folders on new folder open
      setCode('// Folder opened. Select a file to start editing!'); // Clear editor content
      setCurrentFileHandle(null);
      setCurrentFilePath('');
      setShowSidebar(true); // Open sidebar after selecting folder
    } catch (err) {
      console.error('Error opening directory:', err);
      alert('Error opening directory. Make sure you grant permissions.');
    }
  }

  // Open a file from the explorer
  async function openFile(fileHandle, filePath) {
    try {
      const file = await fileHandle.getFile();
      const content = await file.text();
      setCode(content);
      setCurrentFileHandle(fileHandle);
      setCurrentFilePath(filePath);
      setShowSidebar(false); // Close sidebar after opening file
    } catch (err) {
      console.error('Error reading file:', err);
      alert('Error reading file.');
    }
  }

  // Create a new file in the current directory (or root if no folder selected)
  async function createFile() {
    if (!directoryHandle) {
      alert('Please open a folder first.');
      return;
    }
    const fileName = prompt('Enter new file name:');
    if (fileName) {
      try {
        // Determine the target directory handle for creation
        let targetDirHandle = directoryHandle;
        const currentPathParts = currentFilePath.split('/').slice(0, -1); // Get path of current file's directory
        if (currentPathParts.length > 0) {
          for (const part of currentPathParts) {
            targetDirHandle = await targetDirHandle.getDirectoryHandle(part);
          }
        }

        const newFileHandle = await targetDirHandle.getFileHandle(fileName, { create: true });
        const writable = await newFileHandle.createWritable();
        await writable.write(''); // Write empty content
        await writable.close();
        alert(`File "${fileName}" created.`);
        // Rebuild the tree to show the new file
        buildFileTree(directoryHandle).then(setFileTree);
      } catch (err) {
        console.error('Error creating file:', err);
        alert('Error creating file. Check console for details.');
      }
    }
  }

  // Save current editor content to the open file
  async function saveFile() {
    if (!currentFileHandle) {
      alert('No file is currently open to save.');
      return;
    }
    try {
      const writable = await currentFileHandle.createWritable();
      await writable.write(code);
      await writable.close();
      alert('File saved successfully!');
    } catch (err) {
      console.error('Error saving file:', err);
      alert('Error saving file. Make sure you have write permissions.');
    }
  }

  // Upload current file to backend for execution
  async function uploadCurrentFile() {
    if (!currentFileHandle || !currentFilePath) {
      alert('No file is currently open to upload.');
      return;
    }
    try {
      const response = await fetch('/api/upload-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: currentFilePath.split('/').pop(), content: code }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        console.error('Error uploading file:', data.error);
        alert(`Error uploading file: ${data.error}`);
      }
    } catch (error) {
      console.error('Network error:', error);
      alert('Network error while uploading file.');
    }
  }

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  function formatCode() {
    editorRef.current.getAction('editor.action.formatDocument').run();
  }

  function handleEditorChange(value, event) {
    setCode(value);
  }

  function toggleSidebar() {
    setShowSidebar(!showSidebar);
  }

  function clearEditor() {
    setCode('');
    setCurrentFileHandle(null);
    setCurrentFilePath('');
  }

  // Handlers for FileTreeItem
  const handleFileClick = (fileHandle, filePath) => {
    openFile(fileHandle, filePath);
  };

  const handleFolderClick = async (folderHandle, folderPath) => {
    // Toggle expanded state
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(folderPath)) {
        newSet.delete(folderPath);
      } else {
        newSet.add(folderPath);
      }
      return newSet;
    });
  };

  const handleExpandToggle = async (folderHandle, isExpanding) => {
    // This is handled by handleFolderClick now, but kept for clarity if separate logic is needed
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden', position: 'relative' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: '#282c34',
        color: 'white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        zIndex: 10
      }}>
        {/* Hamburger button on the left */}
        <button
          onClick={toggleSidebar}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            fontSize: '1.8em',
            cursor: 'pointer',
            padding: '0',
            lineHeight: '1'
          }}
          title="Menu"
        >
          &#9776;
        </button>
        {/* Format Code button on the right */}
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <button
            onClick={clearEditor}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              fontSize: '1.8em',
              cursor: 'pointer',
              padding: '0',
              lineHeight: '1',
              marginRight: '10px' // Add some space between buttons
            }}
            title="Clear Editor"
          >
            ✖
          </button>
          <button
            onClick={formatCode}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              fontSize: '1.8em',
              cursor: 'pointer',
              padding: '0',
              lineHeight: '1'
            }}
            title="Format Code"
          >
            &lt;/&gt;
          </button>
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
        <Editor
          height="70%" // Editor takes 70% of remaining height
          defaultLanguage="javascript"
          value={code}
          onMount={handleEditorDidMount}
          onChange={handleEditorChange}
          theme="vs-dark"
        />
        <div ref={terminalRef} style={{ height: '30%', backgroundColor: 'black' }} /> {/* Terminal takes 30% */} 
      </div>

      {/* Overlay for when sidebar is open */}
      {showSidebar && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent black
            zIndex: 19, // Below sidebar, above editor
          }}
          onClick={toggleSidebar} // Close sidebar on overlay click
        />
      )}

      {/* Sidebar */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: showSidebar ? '0' : '-300px',
        width: '300px',
        height: '100%',
        backgroundColor: '#222',
        color: 'white',
        boxShadow: '2px 0 5px rgba(0,0,0,0.5)',
        transition: 'left 0.3s ease-in-out',
        zIndex: 20,
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{ padding: '10px', borderBottom: '1px solid #333', display: 'flex', justifyContent: 'space-around', alignItems: 'center' }}>
          <button onClick={openFolder} title="Open Folder" style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5em', cursor: 'pointer' }}>📁</button>
          <button onClick={createFile} title="New File" style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5em', cursor: 'pointer' }}>📄</button>
          <button onClick={saveFile} title="Save File" style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5em', cursor: 'pointer' }}>💾</button>
          <button onClick={uploadCurrentFile} title="Upload Current File" style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5em', cursor: 'pointer' }}>⬆️</button>
        </div>
        <div style={{ flexGrow: 1, overflowY: 'auto', padding: '10px 0' }}>
          {directoryHandle ? (
            fileTree.map((item) => (
              <FileTreeItem
                key={item.path}
                item={item}
                level={0}
                onFileClick={handleFileClick}
                onFolderClick={handleFolderClick}
                onExpandToggle={handleExpandToggle}
              />
            ))
          ) : (
            <p style={{ padding: '0 20px' }}>Click the folder icon to open a directory.</p>
          )}
        </div>
        <div style={{ padding: '10px 20px', borderTop: '1px solid #333' }}>
          <button onClick={toggleSidebar} style={{ width: '100%', padding: '8px', background: '#444', border: 'none', color: 'white', borderRadius: '5px', cursor: 'pointer' }}>Close Explorer</button>
        </div>
      </div>
    </div>
  );
}

export default App;