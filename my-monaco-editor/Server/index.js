import express from 'express';
import expressWs from 'express-ws';
import pty from 'node-pty';
import os from 'os';

const app = express();
const wsInstance = expressWs(app);

const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
const port = 3001;

app.ws('/terminal', (ws, req) => {
  const term = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: process.env.HOME,
    env: process.env
  });

  console.log('Terminal created for client');

  // Pipe terminal output to WebSocket
  term.on('data', (data) => {
    try {
      ws.send(data);
    } catch (ex) {
      // The WebSocket is not open, ignore
    }
  });

  // Pipe WebSocket input to terminal
  ws.on('message', (msg) => {
    term.write(msg);
  });

  // Handle client disconnect
  ws.on('close', () => {
    term.kill();
    console.log('Terminal killed as client disconnected');
  });
});

app.listen(port, () => {
  console.log(`Terminal server listening on port ${port}`);
});