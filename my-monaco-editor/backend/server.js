const express = require('express');
const fs = require('fs');
const path = require('path');



const app = express();
const PORT = 3001;

app.use(express.json());

// Allow CORS for frontend development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

const projectRoot = path.resolve(__dirname, '..'); // Go up one level from backend to my-monaco-editor
const uploadedFilesDir = path.join(__dirname, 'uploaded_files');

// Ensure uploaded_files directory exists
if (!fs.existsSync(uploadedFilesDir)) {
  fs.mkdirSync(uploadedFilesDir, { recursive: true });
}

// Helper to resolve absolute path safely within project root
const resolvePath = (relativePath) => {
  const absolutePath = path.resolve(projectRoot, relativePath);
  if (absolutePath.startsWith(projectRoot)) {
    return absolutePath;
  }
  throw new Error('Access denied: Path outside project root.');
};

// List directory contents
app.get('/api/list-directory', (req, res) => {
  const dirPath = req.query.path || '.';
  try {
    const absolutePath = resolvePath(dirPath);
    fs.readdir(absolutePath, { withFileTypes: true }, (err, files) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      const contents = files.map(file => ({
        name: file.name,
        isDirectory: file.isDirectory(),
      }));
      res.json(contents);
    });
  } catch (e) {
    res.status(403).json({ error: e.message });
  }
});

// Read file content
app.get('/api/read-file', (req, res) => {
  const filePath = req.query.path;
  if (!filePath) {
    return res.status(400).json({ error: 'File path is required.' });
  }
  try {
    const absolutePath = resolvePath(filePath);
    fs.readFile(absolutePath, 'utf8', (err, data) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.send(data);
    });
  } catch (e) {
    res.status(403).json({ error: e.message });
  }
});

// Create new file
app.post('/api/create-file', (req, res) => {
  const { filePath, content = '' } = req.body;
  if (!filePath) {
    return res.status(400).json({ error: 'File path is required.' });
  }
  try {
    const absolutePath = resolvePath(filePath);
    fs.writeFile(absolutePath, content, 'utf8', (err) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.status(201).json({ message: 'File created successfully.' });
    });
  } catch (e) {
    res.status(403).json({ error: e.message });
  }
});

// Save/Update file content
app.post('/api/save-file', (req, res) => {
  const { filePath, content } = req.body;
  if (!filePath || content === undefined) {
    return res.status(400).json({ error: 'File path and content are required.' });
  }
  try {
    const absolutePath = resolvePath(filePath);
    fs.writeFile(absolutePath, content, 'utf8', (err) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ message: 'File saved successfully.' });
    });
  } catch (e) {
    res.status(403).json({ error: e.message });
  }
});

// Upload file to backend's uploaded_files directory
app.post('/api/upload-file', (req, res) => {
  const { filename, content } = req.body;
  if (!filename || content === undefined) {
    return res.status(400).json({ error: 'Filename and content are required.' });
  }

  // Basic sanitization for filename to prevent directory traversal
  const sanitizedFilename = path.basename(filename);
  const targetPath = path.join(uploadedFilesDir, sanitizedFilename);

  fs.writeFile(targetPath, content, 'utf8', (err) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ message: `File ${sanitizedFilename} uploaded successfully to ${uploadedFilesDir}` });
  });
});

const server = app.listen(PORT, () => {
  console.log(`Backend server listening on port ${PORT}`);
});

// WebSocket server for terminal


