"""
flashcard_generator.py
Generates flashcard sets from a topic using Groq LLM.
"""
import json
from groq import Groq

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"


def generate_flashcards(topic: str, level: str, num_cards: int = 10) -> list:
    """Return a list of {front, back} flashcard dicts."""
    prompt = (
        f"Generate {num_cards} flashcards for '{topic}' at {level} level.\n"
        "Return ONLY a JSON object with key 'cards' (array).\n"
        "Each card needs:\n"
        "  - front: a short question or term (max 15 words)\n"
        "  - back: the answer or definition (max 40 words)\n"
        "JSON only, no markdown, no backticks, no extra text."
    )
    try:
        client = Groq(api_key=GROQ_API_KEY)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )
        raw = r.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return data.get("cards", [])
    except Exception as e:
        return [{"front": "Generation failed", "back": str(e)}]
