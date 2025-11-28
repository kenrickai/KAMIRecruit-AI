# memory/memory.py

import os
import json
from typing import Dict, Any, List

MEMORY_DIR = "memory"
os.makedirs(MEMORY_DIR, exist_ok=True)


def memory_path(user_id: int) -> str:
    return os.path.join(MEMORY_DIR, f"user_{user_id}.json")


def _empty_memory() -> Dict[str, Any]:
    return {
        "history": [],        # list[{"sender": "user" | "ai", "message": str}]
        "facts": [],
        "skills": [],
        "preferences": [],
    }


def load_memory(user_id: int) -> Dict[str, Any]:
    path = memory_path(user_id)
    if not os.path.exists(path):
        return _empty_memory()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return _empty_memory()

    # Make sure keys exist even if old file format
    base = _empty_memory()
    base.update(data)
    return base


def save_memory(user_id: int, memory: Dict[str, Any]) -> None:
    path = memory_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def append_history(user_id: int, sender: str, message: str) -> None:
    """
    Adds a single turn to the 'history' list:
    {
      "sender": "user" | "ai",
      "message": "..."
    }
    Keeps only the last 50 turns.
    """
    memory = load_memory(user_id)
    history: List[Dict[str, str]] = memory.get("history", [])
    history.append({"sender": sender, "message": message})
    memory["history"] = history[-50:]
    save_memory(user_id, memory)
