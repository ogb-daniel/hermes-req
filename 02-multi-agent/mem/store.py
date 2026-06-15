
import json
import os
from datetime import datetime


DEFAULT_MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conversation_log.json"
)

def load_memory(filepath=DEFAULT_MEMORY_FILE):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def save_memory(entries, filepath=DEFAULT_MEMORY_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(entries, f, indent=2, default=str)

def add_memory_entry(topic, summary, filepath=DEFAULT_MEMORY_FILE):
    entries = load_memory(filepath)
    entry = {
         "topic": topic,
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
    }
    entries.append(entry)
    save_memory(entries, filepath)
    return entry

def get_memory_context(max_entries=5, filepath=DEFAULT_MEMORY_FILE):
    entries = load_memory(filepath)
    if not entries:
        return ""
    recent = entries[-max_entries:]
    lines = ["Previous research sessions:\n"]
    for entry in recent:
        lines.append(f"### {entry['topic']} ({entry['timestamp'][:10]})")
        lines.append(entry["summary"])
        lines.append("")
    return "\n".join(lines)