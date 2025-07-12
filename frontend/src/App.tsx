import React, { useState, useEffect } from 'react';
import './App.css';
import CodeEditor from './components/Editor';
import FileExplorer from './components/FileExplorer';
import Chat from './components/Chat';
import Terminal from './components/Terminal';
import { useProjectStatus } from './hooks/useProjectStatus'; // Import the hook

// Type Definitions
type SidePanelTab = 'chat' | 'files' | 'agent-activity';

function App() {
  // UI State
  const [isSidePanelOpen, setSidePanelOpen] = useState(true);
  const [activeTab, setActiveTab] = useState<SidePanelTab>('chat');
  const [isBottomTerminalOpen, setBottomTerminalOpen] = useState(false);
  
  // Editor State
  const [currentCode, setCurrentCode] = useState<string>("// Welcome! Start a project in the chat panel.\n");
  const [currentLanguage, setCurrentLanguage] = useState<string>('plaintext');

  // Agent State
  const [runId, setRunId] = useState<string | null>(null);
  const { agentState, isPolling } = useProjectStatus(runId);
  const [refreshFileExplorerKey, setRefreshFileExplorerKey] = useState(0);

  // Effect to watch for agent activity and trigger a file explorer refresh
  useEffect(() => {
    if (agentState?.last_completed_step) {
      // Any step could potentially change files, so we refresh.
      // A more optimized approach might look for specific file-writing steps.
      setRefreshFileExplorerKey(prev => prev + 1);
    }
  }, [agentState]);


  // Event Handlers
  const toggleSidePanel = () => setSidePanelOpen(!isSidePanelOpen);
  const toggleBottomTerminal = () => setBottomTerminalOpen(!isBottomTerminalOpen);

  const handleFileSelect = (code: string, language: string) => {
    setCurrentCode(code);
    setCurrentLanguage(language);
  };
  
  const handleNewProject = (newRunId: string) => {
    setRunId(newRunId);
    setActiveTab('agent-activity');
  };

  const renderSidePanelContent = () => {
    switch (activeTab) {
      case 'chat':
        return <Chat runId={runId} setRunId={handleNewProject} />;
      case 'files':
        return <FileExplorer onFileSelect={handleFileSelect} refreshKey={refreshFileExplorerKey} />;
      case 'agent-activity':
        return <Terminal runId={runId} streamSource="agent" />;
      default:
        return null;
    }
  };
  
  const getStatusIndicator = () => {
      if (!runId) return '⚪ Idle';
      if (isPolling) return '🟢 Working...';
      return '⚫ Finished';
  };

  return (
    <div className="app-container">
      <header className="top-bar">
        <button onClick={toggleSidePanel} className="hamburger-button">☰</button>
        <div className="app-title">Agentic AI Developer</div>
        <div className="status-indicator">{getStatusIndicator()}</div>
      </header>
      
      <div className="main-content">
        {isSidePanelOpen && (
          <aside className="side-panel">
            <div className="side-panel-tabs">
              <button onClick={() => setActiveTab('chat')} className={activeTab === 'chat' ? 'active' : ''}>💬 Chat</button>
              <button onClick={() => setActiveTab('files')} className={activeTab === 'files' ? 'active' : ''}>📄 Files</button>
              <button onClick={() => setActiveTab('agent-activity')} className={activeTab === 'agent-activity' ? 'active' : ''}>🌐 Activity</button>
            </div>
            <div className="side-panel-content">
              {renderSidePanelContent()}
            </div>
          </aside>
        )}
        <div className="content-wrapper">
          <main className="editor-view" style={{ height: isBottomTerminalOpen ? 'calc(100% - 250px)' : 'calc(100% - 30px)'}}>
            <CodeEditor code={currentCode} language={currentLanguage} />
          </main>
          
          <footer className="bottom-terminal" style={{ height: isBottomTerminalOpen ? '250px' : '30px'}}>
             <div className="terminal-header" onClick={toggleBottomTerminal}>
                <span>{`>`} User Terminal</span>
                <span>{isBottomTerminalOpen ? '▼' : '▲'}</span>
             </div>
             <div className="terminal-content-wrapper">
                {isBottomTerminalOpen && <Terminal runId={runId} streamSource="user" />}
             </div>
          </footer>
        </div>
      </div>
    </div>
  );
}

export default App;