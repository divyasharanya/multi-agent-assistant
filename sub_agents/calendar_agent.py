"""Calendar Agent - handles events and scheduling. Powered by Groq."""
import os
from groq import AsyncGroq
from database import get_connection

GROQ_MODEL = "llama-3.3-70b-versatile"

async def call_groq(system_prompt, user_message):
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", ""))
    chat = await client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
        model=GROQ_MODEL, max_tokens=500, temperature=0.5
    )
    return chat.choices[0].message.content

class CalendarAgent:
    async def execute(self, intent, extracted, user_id, original_message):
        actions = []
        if intent == "add_event":
            title = extracted.get("title", "Untitled Event")
            event_date = extracted.get("event_date") or extracted.get("date", "TBD")
            event_time = extracted.get("event_time") or extracted.get("time", None)
            location = extracted.get("location", None)
            conn = get_connection()
            conn.execute("INSERT INTO events (user_id, title, event_date, event_time, location) VALUES (?, ?, ?, ?, ?)", (user_id, title, event_date, event_time, location))
            conn.commit(); conn.close()
            actions.append(f"created_event: {title}")
            response = await call_groq("You are a calendar assistant. Confirm event was added briefly.", f"Event: '{title}' on {event_date} at {event_time or 'TBD'}, location: {location or 'not set'}")
        elif intent == "list_events":
            events = self.get_all_events(user_id)
            actions.append("listed_events")
            if not events:
                response = "Your calendar is empty! Try: 'Schedule meeting on April 10 at 3pm'"
            else:
                event_list = "\n".join([f"- {e['title']} on {e['event_date']} {('at ' + e['event_time']) if e['event_time'] else ''}" for e in events])
                response = await call_groq("You are a calendar assistant. Present events in a friendly way.", f"Events:\n{event_list}")
        elif intent == "delete_event":
            title_hint = extracted.get("title", "")
            conn = get_connection()
            conn.execute("DELETE FROM events WHERE user_id=? AND title LIKE ?", (user_id, f"%{title_hint}%"))
            conn.commit(); conn.close()
            actions.append(f"deleted_event: {title_hint}")
            response = f"🗑️ Removed '{title_hint}' from your calendar."
        else:
            response = await call_groq("You are a calendar assistant.", original_message)
            actions.append("general_calendar_query")
        return response, actions

    def get_all_events(self, user_id):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM events WHERE user_id=? ORDER BY event_date ASC", (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]
