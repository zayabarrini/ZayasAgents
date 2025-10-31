# AudioTranslate Pro

A professional web application for AI-powered audio transcription and translation with multi-language support.

## Features

- **Automatic Transcription**: Convert speech to text with high accuracy
- **Multi-Language Translation**: Translate audio to 8+ languages while preserving voice characteristics
- **Subtitle Generation**: Create perfectly timed subtitles in multiple formats
- **Batch Processing**: Process multiple audio files simultaneously
- **Secure Processing**: Files are processed securely and deleted after conversion

## Project Structure

audio-translate-pro/
│
├── index.html
├── css/
│   ├── main.css
│   ├── components.css
│   └── responsive.css
├── js/
│   ├── main.js
│   ├── file-upload.js
│   ├── transcription.js
│   ├── translation.js
│   ├── batch-processing.js
│   └── utils.js
├── assets/
│   └── icons/
└── README.md



## Setup Instructions

1. Clone or download the project files
2. Open `index.html` in a web browser
3. No build process required - it's a pure frontend application

## Usage

### Transcription
1. Navigate to the "Audio Transcription" tab
2. Upload an audio file (MP3, WAV, M4A, OGG)
3. Select the source language or use auto-detection
4. Click "Transcribe Audio" to generate transcripts and subtitles
5. Download results in TXT, DOCX, SRT, or VTT formats

### Translation
1. Navigate to the "Audio Translation" tab
2. Upload an audio file
3. Select source language and target languages
4. Click "Translate Audio" to generate translated versions
5. Download translated audio and subtitles

### Batch Processing
1. Navigate to the "Batch Processing" tab
2. Upload multiple audio files (up to 10 files, 500MB total)
3. Choose the operation (transcribe, translate, or both)
4. Process all files simultaneously
5. Download results as a ZIP file

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Technologies Used

- Pure HTML5, CSS3, and JavaScript (ES6+)
- CSS Grid and Flexbox for layouts
- Custom event system for component communication
- File API for drag-and-drop uploads
- Audio API for playback controls

