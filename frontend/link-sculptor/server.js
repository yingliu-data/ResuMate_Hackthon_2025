
import express from 'express';
import multer from 'multer';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const upload = multer({ dest: 'uploads/' });
app.use(cors());
app.use(express.json());

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// Ensure logs directory exists
if (!fs.existsSync('logs')) {
  fs.mkdirSync('logs');
}

app.post('/upload', upload.fields([
  { name: 'resume', maxCount: 1 },
  { name: 'jobDescription', maxCount: 1 }
]), (req, res) => {
  const { githubLink, linkedinLink } = req.body;
  const resume = req.files['resume'] ? req.files['resume'][0] : null;
  const jobDescription = req.files['jobDescription'][0];

  // Log the data
  const logData = {
    timestamp: new Date().toISOString(),
    githubLink,
    linkedinLink,
    resumePath: resume ? resume.path : 'No resume uploaded',
    jobDescriptionPath: jobDescription.path
  };

  // Write to log file
  fs.appendFileSync(
    path.join('logs', 'uploads.log'),
    JSON.stringify(logData, null, 2) + '\n---\n',
    'utf8'
  );

  res.json({ message: 'Data received and logged successfully!' });
});

// Add chat endpoint
app.post('/chat', (req, res) => {
  const { message } = req.body;

  // Log chat message
  const logData = {
    timestamp: new Date().toISOString(),
    message,
  };

  fs.appendFileSync(
    path.join('logs', 'chat.log'),
    JSON.stringify(logData, null, 2) + '\n---\n',
    'utf8'
  );

  // Send a simple response (you can enhance this with actual chatbot logic)
  res.json({ message: `I received your message: "${message}". This is a demo response.` });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
