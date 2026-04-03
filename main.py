"""
Multi-Agent Productivity Assistant
===================================
Main FastAPI application entry point.
"""

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from database import init_db
from primary_agent import PrimaryAgent

app = FastAPI(
    title="Multi-Agent Productivity Assistant",
    description="An AI system with multiple agents to manage tasks, schedules & notes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = PrimaryAgent()
app.mount("/static", StaticFiles(directory="."), name="static")

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    actions_taken: list

@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Database initialized")
    print("✅ Server ready at http://localhost:8000")

@app.get("/")
def root():
    return {"status": "running", "message": "Multi-Agent Assistant is live!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await agent.handle(request.message, request.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
def get_tasks(user_id: str = "default_user"):
    from sub_agents.task_agent import TaskAgent
    ta = TaskAgent()
    return ta.get_all_tasks(user_id)

@app.get("/events")
def get_events(user_id: str = "default_user"):
    from sub_agents.calendar_agent import CalendarAgent
    ca = CalendarAgent()
    return ca.get_all_events(user_id)

@app.get("/notes")
def get_notes(user_id: str = "default_user"):
    from sub_agents.notes_agent import NotesAgent
    na = NotesAgent()
    return na.get_all_notes(user_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)