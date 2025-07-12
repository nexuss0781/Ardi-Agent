import React, { useEffect, useRef } from 'react';
import { XTerm } from 'xterm-react';
import { Terminal as XtermTerminal } from 'xterm';
import 'xterm/css/xterm.css';

// --- Component Props ---
interface TerminalProps {
  runId: string | null;
  streamSource: 'agent' | 'user'; // Differentiates the purpose and connection
}

// --- WebSocket Connection Hook ---
const useTerminalSocket = (runId: string | null, termRef: React.RefObject<XTerm | null>) => {
    useEffect(() => {
        const terminal = termRef.current?.terminal;
        if (!runId || !terminal) return;

        terminal.clear();
        terminal.writeln('~ Establishing connection to agent activity stream...');
        
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/terminal/${run_id}`);

        ws.onopen = () => terminal.writeln('~ ✅ Connection established. Awaiting agent activity...');
        ws.onmessage = (event) => terminal.write(event.data);
        ws.onclose = () => terminal.writeln('\r\n~ ❌ Connection to agent activity stream closed.');
        ws.onerror = () => terminal.writeln('\r\n~ ❌ WebSocket connection error.');
        
        return () => ws.close();
    }, [runId, termRef]);
};

// --- Main Component ---
const Terminal: React.FC<TerminalProps> = ({ runId, streamSource }) => {
  const terminalRef = useRef<XTerm>(null);

  // Only the Agent Activity stream connects to the WebSocket to receive logs
  useTerminalSocket(streamSource === 'agent' ? runId : null, terminalRef);
  
  const handleData = (data: string) => {
    // For the USER terminal, we would send this data back to the agent
    if (streamSource === 'user') {
      console.log(`User terminal input (to be implemented): ${data}`);
      // In a full implementation: ws.send(data);
    }
  };

  useEffect(() => {
    const terminal = terminalRef.current?.terminal;
    if (terminal) {
      if (streamSource === 'user') {
        terminal.writeln('~ Interactive User Terminal ~');
        terminal.write('$ ');
      }
    }
  }, [streamSource, terminalRef]);
  
  return (
    <XTerm
      ref={terminalRef}
      onData={handleData}
      options={{
        cursorBlink: true,
        fontSize: 13,
        fontFamily: 'monospace',
        theme: {
          background: '#1e1e1e',
          foreground: '#cccccc',
          cursor: '#ffffff',
        },
        rows: 15,
      }}
      className="terminal-component"
    />
  );
};

export default Terminal;