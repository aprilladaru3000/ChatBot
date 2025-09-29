from typing import Dict, List, Optional
import uuid


# In-memory store: session_id -> list of {'question': str, 'answer': str, 'source': str, 'feedback': Optional[str]}
_SESSIONS: Dict[str, List[Dict[str, Optional[str]]]] = {}


def create_session() -> str:
    session_id = str(uuid.uuid4())
    _SESSIONS[session_id] = []
    return session_id


def add_turn(session_id: str, question: str, answer: str, source: str) -> None:
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = []
    _SESSIONS[session_id].append({'question': question, 'answer': answer, 'source': source, 'feedback': None})


# Feedback feature
def add_feedback(session_id: str, turn_index: int, feedback: str) -> bool:
    """Add feedback to a specific turn in the session history."""
    turns = _SESSIONS.get(session_id)
    if turns and 0 <= turn_index < len(turns):
        turns[turn_index]['feedback'] = feedback
        return True
    return False


def get_history(session_id: str):
    return _SESSIONS.get(session_id, [])


def clear_session(session_id: str) -> bool:
    if session_id in _SESSIONS:
        _SESSIONS[session_id] = []
        return True
    return False
