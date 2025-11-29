# 🚀 LinkedIn AI Post Generator

A Chrome extension that uses AI to generate engaging LinkedIn posts.

## Features
- AI-powered post generation using Google Gemini
- Multiple tone options (Professional, Casual, Inspiring, etc.)
- One-click copy to clipboard
- Beautiful, modern UI

## Setup

### Backend
1. Install dependencies:
```bash
   pip install fastapi uvicorn requests pydantic
```

2. Set your Gemini API key:
```bash
   export GEMINI_API_KEY="your-api-key-here"
```

3. Run the server:
```bash
   python backend/main.py
```

### Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` folder
5. Click the extension icon and start generating posts!

## Tech Stack
- Backend: FastAPI, Python
- Frontend: HTML, CSS, JavaScript
- AI: Google Gemini API# LinkedIn AI Post Generator
