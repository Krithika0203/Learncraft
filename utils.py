"""
utils.py
Helper utilities: progress persistence, notes, topic lists, learning paths, etc.
"""
import json
import os
from datetime import date

PROGRESS_FILE = "learning_progress.json"
NOTES_FILE = "notes.json"

TOPICS = [
    "Photosynthesis",
    "Machine Learning",
    "World War II",
    "Python Functions",
    "Calculus",
    "Climate Change",
    "The French Revolution",
    "DNA Replication",
    "Object-Oriented Programming",
    "The Solar System",
    "Economics Supply & Demand",
    "Quantum Mechanics",
]

LEARNING_PATHS = {
    "machine learning": ["Python Functions", "Calculus", "Economics Supply & Demand", "Machine Learning"],
    "quantum mechanics": ["Calculus", "The Solar System", "Quantum Mechanics"],
    "dna replication": ["Photosynthesis", "DNA Replication"],
    "calculus": ["Python Functions", "Calculus"],
    "object-oriented programming": ["Python Functions", "Object-Oriented Programming"],
    "climate change": ["Photosynthesis", "Economics Supply & Demand", "Climate Change"],
}


def get_topics() -> list:
    return sorted(TOPICS)


def load_progress() -> dict:
    """Load progress from JSON file, or return empty structure."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "topics_studied": [],
        "scores": [],
        "best_score": 0,
        "topic_scores": {},   # {topic: best_score_int}
        "sessions": [],       # [{topic, score, date}]
    }


def save_progress(progress: dict, topic: str = None, score: int = None) -> None:
    """Update and persist progress data."""
    if "topic_scores" not in progress:
        progress["topic_scores"] = {}
    if "sessions" not in progress:
        progress["sessions"] = []

    if topic:
        studied = progress.get("topics_studied", [])
        if topic not in studied:
            studied.append(topic)
        progress["topics_studied"] = studied

    if score is not None:
        scores = progress.get("scores", [])
        scores.append(score)
        progress["scores"] = scores
        if score > progress.get("best_score", 0):
            progress["best_score"] = score

        # Per-topic best score (store single int, not list)
        if topic:
            ts = progress["topic_scores"]
            existing = ts.get(topic, 0)
            # Handle legacy list format
            if isinstance(existing, list):
                existing = max(existing) if existing else 0
            ts[topic] = max(existing, score)
            progress["topic_scores"] = ts

        # Session log
        sessions = progress.get("sessions", [])
        sessions.append({
            "topic": topic or "Unknown",
            "score": score,
            "date": str(date.today())
        })
        progress["sessions"] = sessions

    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
    except IOError:
        pass


def get_weak_topics(progress: dict) -> list:
    """Return topics where the best score is below 60%."""
    result = []
    for topic, score in progress.get("topic_scores", {}).items():
        # Handle legacy list format
        if isinstance(score, list):
            score = max(score) if score else 0
        if score < 60:
            result.append(topic)
    return result


def get_learning_path(topic: str) -> list:
    """Return recommended learning path for a topic, or empty list."""
    return LEARNING_PATHS.get(topic.lower().strip(), [])


# ── Notes ────────────────────────────────────────────────────────────────────

def load_notes() -> list:
    """Load saved notes from JSON file."""
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_note(note_text: str, topic: str) -> None:
    """Append a note and persist to file."""
    notes = load_notes()
    notes.append({
        "topic": topic,
        "note": note_text,
        "date": str(date.today())
    })
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except IOError:
        pass


def delete_note(index: int) -> None:
    """Delete a note by its index."""
    notes = load_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except IOError:
        pass