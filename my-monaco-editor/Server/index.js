import express from 'express';
import expressWs from 'express-ws';
import pty from 'node-pty';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

// --- Setup for serving static files ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// ------------------------------------

const app = express();
expressWs(app);

const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
const port = process.env.PORT || 3001;

// --- Serve the built Vite frontend ---
// This tells Express to look in the 'dist' folder for static files (index.html, css, js)
const frontendDistPath = path.join(__dirname, '..', 'dist');
app.use(express.static(frontendDistPath));
// -----------------------------------

// --- WebSocket endpoint for the terminal ---
app.ws('/terminal', (ws, req) => {
  const term = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: process.env.HOME,
    env: process.env
  });

  console.log('Terminal created for client');

  term.on('data', (data) => {
    try {
      ws.send(data);
    } catch (ex) { /* ignore */ }
  });

  ws.on('message', (msg) => {
    term.write(msg);
  });

  ws.on('close', () => {
    term.kill();
    console.log('Terminal killed as client disconnected');
  });
});
// ----------------------------------------

// --- Catch-all to serve index.html for any other GET request ---
// This is crucial for Single Page Applications (SPAs)
app.get('*', (req, res) => {
  res.sendFile(path.join(frontendDistPath, 'index.html'));
});
// -------------------------------------------------------------

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
