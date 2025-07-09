import React, { useEffect, useRef } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';
import { useUIStore } from '../store/uiStore';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

const Terminal = () => {
  const { isTerminalOpen, toggleTerminal } = useUIStore((state) => ({
    isTerminalOpen: state.isTerminalOpen,
    toggleTerminal: state.toggleTerminal,
  }));
  const termRef = useRef(null);
  const termContainerRef = useRef(null);

  useEffect(() => {
    if (!isTerminalOpen || !termContainerRef.current) return;

    if (termRef.current) { // If terminal already exists, just fit it.
      const fitAddon = termRef.current.fitAddon;
      fitAddon.fit();
      return;
    }

    const term = new XTerm({
      cursorBlink: true,
      fontSize: 13,
      fontFamily: 'monospace',
      theme: {
        background: '#1e1e1e',
        foreground: '#d4d4d4',
      },
      rows: 10,
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);

    term.open(termContainerRef.current);
    fitAddon.fit();

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${protocol}://${window.location.host}/terminal`;
    const socket = new WebSocket(url);

    socket.onopen = () => {
      term.write('Connected to backend terminal...\r\n');
      fitAddon.fit();
    };

    socket.onmessage = (ev) => {
      term.write(typeof ev.data === 'string' ? ev.data : new Uint8Array(ev.data));
    };

    socket.onclose = () => {
      term.write('\r\nConnection closed.\r\n');
    };

    socket.onerror = (err) => {
      console.error('Socket error:', err);
      term.write('\r\nError connecting to terminal server.\r\n');
    };

    term.onData((data) => {
      socket.send(data);
    });
    
    termRef.current = { term, fitAddon, socket };

    const resizeObserver = new ResizeObserver(() => {
        fitAddon.fit();
    });
    resizeObserver.observe(termContainerRef.current);

    return () => {
      resizeObserver.disconnect();
      socket.close();
      term.dispose();
      termRef.current = null;
    };
  }, [isTerminalOpen]);

  return (
    <div className="bg-[#252526] shrink-0 flex flex-col">
      <div 
        className="flex items-center h-8 px-4 text-xs font-mono border-t border-t-[#333333] cursor-pointer shrink-0"
        onClick={toggleTerminal}
      >
        <span className="flex-1 uppercase">Terminal</span>
        <button className="focus:outline-none">
          {isTerminalOpen ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
        </button>
      </div>
      {isTerminalOpen && (
        <div 
          ref={termContainerRef}
          className="flex-1 p-1"
          style={{ height: '240px' }} // Default height, gets managed by flex
        >
        </div>
      )}
    </div>
  );
};

export default Terminal;