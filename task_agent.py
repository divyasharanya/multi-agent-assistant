"""Task Agent - handles to-dos and tasks. Powered by Groq."""
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

class TaskAgent:
    async def execute(self, intent, extracted, user_id, original_message):
        actions = []
        if intent == "add_task":
            title = extracted.get("title", original_message[:50])
            due_date = extracted.get("due_date", None)
            priority = extracted.get("priority", "medium")
            conn = get_connection()
            conn.execute("INSERT INTO tasks (user_id, title, due_date, priority) VALUES (?, ?, ?, ?)", (user_id, title, due_date, priority))
            conn.commit(); conn.close()
            actions.append(f"created_task: {title}")
            response = await call_groq("You are a friendly assistant. Confirm task creation briefly.", f"Task added: '{title}', due: {due_date}, priority: {priority}")
        elif intent == "list_tasks":
            tasks = self.get_all_tasks(user_id)
            actions.append("listed_tasks")
            if not tasks:
                response = "You have no tasks! Add one by saying 'Add task: [name]'"
            else:
                task_list = "\n".join([f"- [{t['status']}] {t['title']} (due: {t['due_date'] or 'no date'}, {t['priority']} priority)" for t in tasks])
                response = await call_groq("You are a productivity assistant. Present this task list in a friendly way.", f"Tasks:\n{task_list}")
        elif intent == "complete_task":
            title_hint = extracted.get("title", "")
            conn = get_connection()
            conn.execute("UPDATE tasks SET status='done' WHERE user_id=? AND title LIKE ? AND status='pending'", (user_id, f"%{title_hint}%"))
            conn.commit(); conn.close()
            actions.append(f"completed_task: {title_hint}")
            response = f"✅ Marked '{title_hint}' as done!"
        elif intent == "delete_task":
            title_hint = extracted.get("title", "")
            conn = get_connection()
            conn.execute("DELETE FROM tasks WHERE user_id=? AND title LIKE ?", (user_id, f"%{title_hint}%"))
            conn.commit(); conn.close()
            actions.append(f"deleted_task: {title_hint}")
            response = f"🗑️ Deleted tasks matching '{title_hint}'."
        else:
            response = await call_groq("You are a task management assistant.", original_message)
            actions.append("general_task_query")
        return response, actions

    def get_all_tasks(self, user_id):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM tasks WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]