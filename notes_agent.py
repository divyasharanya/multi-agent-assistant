"""Notes Agent - handles note-taking. Powered by Groq."""
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

class NotesAgent:
    async def execute(self, intent, extracted, user_id, original_message):
        actions = []
        if intent == "add_note":
            title = extracted.get("title", "Quick Note")
            content = extracted.get("content") or original_message
            tags = extracted.get("tags", "")
            conn = get_connection()
            conn.execute("INSERT INTO notes (user_id, title, content, tags) VALUES (?, ?, ?, ?)", (user_id, title, content, tags))
            conn.commit(); conn.close()
            actions.append(f"created_note: {title}")
            response = await call_groq("You are a notes assistant. Confirm note was saved briefly.", f"Note saved: '{title}'")
        elif intent == "list_notes":
            notes = self.get_all_notes(user_id)
            actions.append("listed_notes")
            if not notes:
                response = "No notes yet! Try: 'Note: [your idea]'"
            else:
                note_list = "\n".join([f"- {n['title']}: {n['content'][:60]}..." for n in notes])
                response = await call_groq("You are a notes assistant. Present notes in a friendly way.", f"Notes:\n{note_list}")
        elif intent == "search_notes":
            keyword = extracted.get("keyword") or extracted.get("title", "")
            conn = get_connection()
            rows = conn.execute("SELECT * FROM notes WHERE user_id=? AND (title LIKE ? OR content LIKE ?)", (user_id, f"%{keyword}%", f"%{keyword}%")).fetchall()
            conn.close()
            results = [dict(r) for r in rows]
            actions.append(f"searched_notes: {keyword}")
            response = f"Found {len(results)} note(s) for '{keyword}':\n" + "\n".join([f"- {n['title']}: {n['content'][:80]}" for n in results]) if results else f"No notes found for '{keyword}'."
        elif intent == "delete_note":
            title_hint = extracted.get("title", "")
            conn = get_connection()
            conn.execute("DELETE FROM notes WHERE user_id=? AND title LIKE ?", (user_id, f"%{title_hint}%"))
            conn.commit(); conn.close()
            actions.append(f"deleted_note: {title_hint}")
            response = f"🗑️ Deleted notes matching '{title_hint}'."
        else:
            response = await call_groq("You are a notes assistant.", original_message)
            actions.append("general_notes_query")
        return response, actions

    def get_all_notes(self, user_id):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM notes WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]