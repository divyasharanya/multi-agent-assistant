# 🤖 Multi-Agent Productivity Assistant
### Hack2Skill Gen AI Academy APAC Edition — Hackathon Submission

---

## 📌 What This Project Does

A multi-agent AI system that helps users manage:
- ✅ **Tasks** (to-dos, priorities, deadlines)
- 📅 **Calendar Events** (meetings, appointments)
- 📝 **Notes** (ideas, memos, information)

The user just types naturally in plain English. The **Primary Agent** (powered by Claude AI)
automatically decides which **Sub-Agent** to call, performs the action, and responds.

---

## 🏗️ Architecture

```
User Message
     │
     ▼
Primary Agent (Claude AI)
     │ Classifies intent
     ├──► Task Agent      → SQLite (tasks table)
     ├──► Calendar Agent  → SQLite (events table)
     └──► Notes Agent     → SQLite (notes table)
     │
     ▼
FastAPI Response → Frontend UI
```

---

## 🚀 Setup Instructions (Step by Step)

### Step 1: Get your Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up / log in
3. Click "API Keys" → "Create Key"
4. Copy the key (starts with `sk-ant-...`)

### Step 2: Set up the project
```bash
# 1. Navigate to the project folder
cd multi_agent_assistant

# 2. Create a virtual environment (keeps dependencies isolated)
python -m venv venv

# 3. Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Step 3: Add your API key
```bash
# Create a .env file
cp .env.example .env

# Open .env and replace "your_api_key_here" with your actual key
# The file should look like:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
```

### Step 4: Run the server
```bash
# Set environment variable (Mac/Linux)
export ANTHROPIC_API_KEY=your_key_here

# Or on Windows:
set ANTHROPIC_API_KEY=your_key_here

# Start the server
python main.py
```

### Step 5: Open the frontend
Open `frontend.html` in your browser — that's it! 🎉

---

## 💬 Example Commands

| What you say | Which agent handles it |
|---|---|
| "Add task: finish slides by 5pm, high priority" | Task Agent |
| "Show all my tasks" | Task Agent |
| "Mark complete: finish slides" | Task Agent |
| "Schedule team meeting on April 10 at 3pm" | Calendar Agent |
| "What events do I have?" | Calendar Agent |
| "Note: The API endpoint is /chat" | Notes Agent |
| "Show my notes" | Notes Agent |
| "Search notes for API" | Notes Agent |

---

## 📁 Project Structure

```
multi_agent_assistant/
├── main.py              ← FastAPI server, all API endpoints
├── primary_agent.py     ← Brain: routes messages to correct sub-agent
├── database.py          ← SQLite setup, creates tables
├── frontend.html        ← Web UI (open in browser)
├── requirements.txt     ← Python packages needed
├── .env.example         ← Template for your API key
└── sub_agents/
    ├── task_agent.py     ← Handles tasks/to-dos
    ├── calendar_agent.py ← Handles events/schedule
    └── notes_agent.py    ← Handles notes/memos
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/chat` | Main chat endpoint |
| GET | `/tasks` | Get all tasks |
| GET | `/events` | Get all events |
| GET | `/notes` | Get all notes |

### Example API call:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task: submit hackathon project", "user_id": "me"}'
```

---

## 🧪 Test the API directly
Once the server is running, visit: **http://localhost:8000/docs**
This gives you an interactive Swagger UI to test all endpoints!

---

## ✅ Hackathon Requirements Checklist

- [x] Primary agent coordinating sub-agents ✅
- [x] SQLite database for structured data ✅
- [x] Multiple tools (task/calendar/notes) via agent routing ✅
- [x] Multi-step workflows and task execution ✅
- [x] Deployed as API-based system (FastAPI) ✅
- [x] Frontend UI for demonstration ✅
