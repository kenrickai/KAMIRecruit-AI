import json
import os
from typing import Dict, Any, List


MEMORY_DIR = "memory_store"
os.makedirs(MEMORY_DIR, exist_ok=True)


def _memory_path(user_id: int) -> str:
    return os.path.join(MEMORY_DIR, f"user_{user_id}.json")


def load_memory(user_id: int) -> Dict[str, Any]:
    """
    Loads memory for a user from disk.
    Returns an empty dict if nothing exists yet.
    """
    path = _memory_path(user_id)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(user_id: int, memory: Dict[str, Any]) -> None:
    path = _memory_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def append_history(user_id: int, sender: str, message: str) -> None:
    """
    Adds a single turn to the 'history' list:
    { "sender": "user" | "ai", "message": "..." }
    Keeps only the last 50 turns.
    """
    memory = load_memory(user_id)
    history: List[Dict[str, str]] = memory.get("history", [])
    history.append({"sender": sender, "message": message})
    memory["history"] = history[-50:]
    save_memory(user_id, memory)
