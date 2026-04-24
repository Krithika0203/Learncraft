import json
from groq import Groq

STYLE_TIMES = {
    "Summary Notes": "3-5 min",
    "Detailed Explanation": "8-12 min",
    "Bullet Points": "2-4 min",
    "Concept Map": "5-7 min"
}

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"


def generate_content(topic, level, content_style, focus=""):
    focus_note = " Focus specifically on: " + focus + "." if focus else ""
    prompt = (
        "Generate structured study notes for '" + topic + "' at " + level + " level "
        "in the style of " + content_style + "." + focus_note + "\n\n"
        "Return ONLY a JSON object with:\n"
        "- sections: array of 3 objects each with 'title' and 'content'\n"
        "- key_terms: array of 4-6 objects each with 'term' and 'definition'\n"
        "- summary: one string (1-2 sentences)\n\n"
        "JSON only, no markdown, no backticks, no extra text."
    )

    try:
        client = Groq(api_key=GROQ_API_KEY)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        raw = r.choices[0].message.content.strip()
        # Strip markdown fences if model adds them anyway
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return {
            "topic": topic.title(),
            "level": level,
            "style": content_style,
            "read_time": STYLE_TIMES.get(content_style, "5 min"),
            "sections": data["sections"],
            "key_terms": data["key_terms"],
            "summary": data["summary"],
            "ai_generated": True,
        }
    except Exception as e:
        # Graceful fallback so the app never crashes
        return {
            "topic": topic.title(),
            "level": level,
            "style": content_style,
            "read_time": STYLE_TIMES.get(content_style, "5 min"),
            "sections": [
                {"title": "Overview", "content": f"Study notes for {topic} at {level} level could not be generated. Please try again."},
            ],
            "key_terms": [],
            "summary": f"Content generation failed: {str(e)}",
            "ai_generated": False,
        }