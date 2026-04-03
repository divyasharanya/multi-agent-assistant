"""
Primary Agent - powered by Groq (free & fast!)
Routes user messages to the correct sub-agent.
"""
import json, os
from groq import AsyncGroq
from sub_agents.task_agent import TaskAgent
from sub_agents.calendar_agent import CalendarAgent
from sub_agents.notes_agent import NotesAgent

GROQ_MODEL = "llama-3.3-70b-versatile"

async def call_groq(system_prompt: str, user_message: str) -> str:
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", ""))
    chat = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        model=GROQ_MODEL,
        max_tokens=1000,
        temperature=0.3
    )
    return chat.choices[0].message.content

class PrimaryAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
        self.calendar_agent = CalendarAgent()
        self.notes_agent = NotesAgent()
        self.routing_prompt = """
You are a routing agent for a productivity assistant. Classify the user message into the correct sub-agent.

Sub-agents available:
- task_agent: for tasks/to-dos
- calendar_agent: for events/meetings/schedule
- notes_agent: for notes/memos/ideas
- general: for greetings, help, or unknown requests

Respond ONLY with valid JSON (no markdown, no explanation):
{"agent": "task_agent", "intent": "add_task", "extracted_info": {"title": "...", "due_date": "YYYY-MM-DD or null", "priority": "low/medium/high"}}

Intent options:
- task_agent: add_task, list_tasks, complete_task, delete_task
- calendar_agent: add_event, list_events, delete_event
- notes_agent: add_note, list_notes, search_notes, delete_note
- general: greet, help, unknown
"""

    async def handle(self, user_message: str, user_id: str) -> dict:
        # Step 1: Route the message
        routing_response = await call_groq(self.routing_prompt, user_message)
        try:
            clean = routing_response.strip().replace("```json", "").replace("```", "").strip()
            routing = json.loads(clean)
        except Exception:
            routing = {"agent": "general", "intent": "unknown", "extracted_info": {}}

        agent_name = routing.get("agent", "general")
        intent = routing.get("intent", "unknown")
        extracted = routing.get("extracted_info", {})

        # Step 2: Delegate to the right agent
        if agent_name == "task_agent":
            result, actions = await self.task_agent.execute(intent, extracted, user_id, user_message)
        elif agent_name == "calendar_agent":
            result, actions = await self.calendar_agent.execute(intent, extracted, user_id, user_message)
        elif agent_name == "notes_agent":
            result, actions = await self.notes_agent.execute(intent, extracted, user_id, user_message)
        else:
            result = await call_groq(
                "You are a helpful productivity assistant. Be concise and friendly.",
                user_message
            )
            actions = ["general_response"]

        return {
            "response": result,
            "agent_used": agent_name,
            "actions_taken": actions
        }