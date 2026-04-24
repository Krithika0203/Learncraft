"""
gamification.py
Handles XP, streaks, badges, and levels for LearnCraft.
"""
import json
import os
from datetime import date, timedelta

GAMIFICATION_FILE = "gamification.json"

# ── XP values ────────────────────────────────────────────────────────────────
XP_STUDY_SESSION  = 10
XP_QUIZ_COMPLETE  = 20
XP_PERFECT_SCORE  = 50
XP_SCORE_ABOVE_80 = 30
XP_SCORE_ABOVE_60 = 15
XP_FLASHCARD_DECK = 10
XP_STREAK_BONUS   = 5   # per day of streak

# ── Level thresholds ─────────────────────────────────────────────────────────
LEVELS = [
    (0,    "🌱 Seedling"),
    (50,   "📖 Reader"),
    (150,  "🎓 Student"),
    (300,  "🔬 Scholar"),
    (500,  "🏆 Expert"),
    (800,  "🌟 Master"),
    (1200, "🚀 Genius"),
]

# ── Badge definitions ─────────────────────────────────────────────────────────
BADGES = {
    "first_quiz":       {"name": "First Quiz",        "icon": "🎯", "desc": "Complete your first quiz"},
    "perfect_score":    {"name": "Perfect Score",     "icon": "💯", "desc": "Score 100% on a quiz"},
    "streak_3":         {"name": "3-Day Streak",      "icon": "🔥", "desc": "Study 3 days in a row"},
    "streak_7":         {"name": "Week Warrior",      "icon": "⚡", "desc": "Study 7 days in a row"},
    "streak_14":        {"name": "Fortnight Hero",    "icon": "🗓️", "desc": "Study 14 days in a row"},
    "topics_5":         {"name": "Explorer",          "icon": "🗺️", "desc": "Study 5 different topics"},
    "topics_10":        {"name": "Polymath",          "icon": "🧠", "desc": "Study 10 different topics"},
    "quizzes_10":       {"name": "Quiz Master",       "icon": "🧩", "desc": "Complete 10 quizzes"},
    "quizzes_25":       {"name": "Quiz Champion",     "icon": "🏅", "desc": "Complete 25 quizzes"},
    "score_above_80":   {"name": "High Achiever",     "icon": "🎉", "desc": "Score above 80% on a quiz"},
    "flashcards":       {"name": "Card Shark",        "icon": "🃏", "desc": "Complete a flashcard deck"},
    "level_scholar":    {"name": "Scholar",           "icon": "🔬", "desc": "Reach Scholar level (300 XP)"},
    "level_expert":     {"name": "Expert",            "icon": "🏆", "desc": "Reach Expert level (500 XP)"},
    "level_master":     {"name": "Master",            "icon": "🌟", "desc": "Reach Master level (800 XP)"},
    "notes_saver":      {"name": "Note Taker",        "icon": "📝", "desc": "Save your first note"},
}


def load_gamification() -> dict:
    if os.path.exists(GAMIFICATION_FILE):
        try:
            with open(GAMIFICATION_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "xp": 0,
        "badges": [],
        "streak": 0,
        "last_study_date": None,
        "total_quizzes": 0,
        "study_dates": [],
    }


def save_gamification(data: dict) -> None:
    try:
        with open(GAMIFICATION_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


def get_level(xp: int) -> tuple:
    """Return (level_name, xp_for_next, xp_in_current_level, progress_pct)."""
    current_level = LEVELS[0]
    next_level    = None
    for i, (threshold, name) in enumerate(LEVELS):
        if xp >= threshold:
            current_level = (threshold, name)
            next_level    = LEVELS[i + 1] if i + 1 < len(LEVELS) else None
    if next_level:
        xp_start = current_level[0]
        xp_end   = next_level[0]
        progress = (xp - xp_start) / (xp_end - xp_start)
        return current_level[1], next_level[1], xp_end - xp, round(progress * 100)
    return current_level[1], None, 0, 100


def update_streak(data: dict) -> dict:
    today     = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    last      = data.get("last_study_date")

    study_dates = data.get("study_dates", [])
    if today not in study_dates:
        study_dates.append(today)
    data["study_dates"] = study_dates

    if last == today:
        pass  # already counted today
    elif last == yesterday:
        data["streak"] = data.get("streak", 0) + 1
        data["last_study_date"] = today
    else:
        data["streak"] = 1
        data["last_study_date"] = today

    return data


def award_xp(data: dict, amount: int, reason: str = "") -> tuple:
    """Add XP and return (new_data, xp_awarded, level_up_msg)."""
    old_xp    = data.get("xp", 0)
    old_level = get_level(old_xp)[0]
    data["xp"] = old_xp + amount
    new_level = get_level(data["xp"])[0]
    level_up  = new_level if new_level != old_level else None
    return data, amount, level_up


def check_and_award_badges(data: dict, context: dict) -> list:
    """
    Check badge conditions and award new ones.
    context keys: score, topics_count, quizzes_count, event
    Returns list of newly awarded badge keys.
    """
    earned    = set(data.get("badges", []))
    new_ones  = []

    score          = context.get("score", -1)
    topics_count   = context.get("topics_count", 0)
    quizzes_count  = context.get("quizzes_count", 0)
    event          = context.get("event", "")
    streak         = data.get("streak", 0)
    xp             = data.get("xp", 0)

    checks = {
        "first_quiz":     quizzes_count >= 1,
        "perfect_score":  score == 100,
        "streak_3":       streak >= 3,
        "streak_7":       streak >= 7,
        "streak_14":      streak >= 14,
        "topics_5":       topics_count >= 5,
        "topics_10":      topics_count >= 10,
        "quizzes_10":     quizzes_count >= 10,
        "quizzes_25":     quizzes_count >= 25,
        "score_above_80": score >= 80,
        "flashcards":     event == "flashcards",
        "level_scholar":  xp >= 300,
        "level_expert":   xp >= 500,
        "level_master":   xp >= 800,
        "notes_saver":    event == "note_saved",
    }

    for key, condition in checks.items():
        if condition and key not in earned:
            earned.add(key)
            new_ones.append(key)

    data["badges"] = list(earned)
    return new_ones


def record_quiz(data: dict, score: int, topics_count: int) -> dict:
    data["total_quizzes"] = data.get("total_quizzes", 0) + 1
    return data


def get_xp_for_quiz(score: int) -> int:
    xp = XP_QUIZ_COMPLETE
    if score == 100:
        xp += XP_PERFECT_SCORE
    elif score >= 80:
        xp += XP_SCORE_ABOVE_80
    elif score >= 60:
        xp += XP_SCORE_ABOVE_60
    return xp
