import express from 'express';
import expressWs from 'express-ws';
import pty from 'node-pty';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
expressWs(app);

const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
const port = process.env.PORT || 3001;

const frontendDistPath = path.join(__dirname, '..', 'dist');
app.use(express.static(frontendDistPath));

app.ws('/terminal', (ws, req) => {
  // --- THE FIX ---
  // We change the starting directory from process.env.HOME to the project's root folder.
  const projectRoot = path.resolve(__dirname, '..');
  // ---------------

  const term = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: projectRoot, // <-- THIS LINE IS THE ONLY CHANGE
    env: process.env
  });

  console.log(`Terminal created for client in directory: ${projectRoot}`);

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

app.get('*', (req, res) => {
  res.sendFile(path.join(frontendDistPath, 'index.html'));
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
