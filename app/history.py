from typing import Dict, List
import uuid

# In-memory store: session_id -> list of {'question': str, 'answer': str, 'source': str}
_SESSIONS: Dict[str, List[Dict[str, str]]] = {}


def create_session() -> str:
    session_id = str(uuid.uuid4())
    _SESSIONS[session_id] = []
    return session_id


def add_turn(session_id: str, question: str, answer: str, source: str) -> None:
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = []
    _SESSIONS[session_id].append({'question': question, 'answer': answer, 'source': source})


def get_history(session_id: str):
    return _SESSIONS.get(session_id, [])


def clear_session(session_id: str) -> bool:
    if session_id in _SESSIONS:
        _SESSIONS[session_id] = []
        return True
    return False
