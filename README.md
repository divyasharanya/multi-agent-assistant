# 🤖 Multi-Agent Productivity Assistant
### Hack2Skill Gen AI Academy APAC Edition — Hackathon Submission

---

## 🌐 Live Demo
- **Live App:** https://multi-agent-assistant-n3bq.onrender.com/static/frontend.html
- **API:** https://multi-agent-assistant-n3bq.onrender.com
- **API Docs:** https://multi-agent-assistant-n3bq.onrender.com/docs
- **GitHub:** https://github.com/divyasharanya/multi-agent-assistant

---

## 📌 What This Project Does

A multi-agent AI system that helps users manage:
- ✅ **Tasks** (to-dos, priorities, deadlines)
- 📅 **Calendar Events** (meetings, appointments)
- 📝 **Notes** (ideas, memos, information)

The user just types naturally in plain English. The **Primary Agent** (powered by Groq LLaMA) automatically decides which **Sub-Agent** to call, performs the action, and responds.

---

## 🏗️ Architecture

```
User Message
     │
     ▼
Primary Agent (Groq LLaMA)
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

### Step 1: Get your FREE Groq API Key
1. Go to https://console.groq.com/
2. Sign up / log in
3. Click **"API Keys"** → **"Create Key"**
4. Copy the key (starts with `gsk_...`)

### Step 2: Set up the project
```bash
# 1. Clone the repository
git clone https://github.com/divyasharanya/multi-agent-assistant.git
cd multi-agent-assistant

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Step 3: Set your API key
```bash
# On Mac/Linux:
export GROQ_API_KEY=your_key_here

# On Windows:
$env:GROQ_API_KEY="your_key_here"
```

### Step 4: Run the server
```bash
python main.py
```

### Step 5: Open the frontend
Open `frontend.html` in your browser — that's it! 🎉

Or visit: **http://localhost:8000/static/frontend.html**

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
multi-agent-assistant/
├── main.py              ← FastAPI server, all API endpoints
├── primary_agent.py     ← Brain: routes messages to correct sub-agent
├── database.py          ← SQLite setup, creates tables
├── frontend.html        ← Web UI
├── requirements.txt     ← Python packages needed
└── sub_agents/
    ├── __init__.py
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
curl -X POST https://multi-agent-assistant-n3bq.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task: submit hackathon project", "user_id": "me"}'
```

---

## 🧪 Test the API
Visit: **https://multi-agent-assistant-n3bq.onrender.com/docs**

This gives you an interactive Swagger UI to test all endpoints!

---

## ✅ Hackathon Requirements Checklist

- [x] Primary agent coordinating sub-agents ✅
- [x] SQLite database for structured data ✅
- [x] Multiple tools (task/calendar/notes) via agent routing ✅
- [x] Multi-step workflows and task execution ✅
- [x] Deployed as API-based system (FastAPI on Render) ✅
- [x] Frontend UI for demonstration ✅
- [x] Live deployment with permanent URL ✅
