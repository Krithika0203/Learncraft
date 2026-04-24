import json
from groq import Groq

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"


def generate_quiz(topic, level, num_questions, q_type):
    if q_type != "Mixed":
        type_instruction = "All questions must be type: " + q_type + "."
    else:
        type_instruction = "Mix these types: Multiple Choice, True/False, Fill in the Blank, Short Answer."

    prompt = (
        "Generate " + str(num_questions) + " quiz questions about '" + topic + "' at " + level + " level.\n"
        + type_instruction + "\n\n"
        "Return ONLY a JSON object with key 'questions' (array).\n"
        "Each question needs:\n"
        "  - type: one of 'Multiple Choice', 'True/False', 'Fill in the Blank', 'Short Answer'\n"
        "  - question: the question text (for Fill in the Blank, use ___ for the blank)\n"
        "  - options: 4 strings for MC, ['True','False'] for TF, [] for others\n"
        "  - answer: the correct answer string\n"
        "  - explanation: one sentence explaining why\n\n"
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
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return {
            "title": topic.title() + " Quiz",
            "topic": topic.title(),
            "difficulty": level,
            "questions": data["questions"]
        }
    except Exception as e:
        # Fallback single question so app never crashes
        return {
            "title": topic.title() + " Quiz",
            "topic": topic.title(),
            "difficulty": level,
            "questions": [
                {
                    "type": "Short Answer",
                    "question": f"Quiz generation failed ({str(e)}). Please retry.",
                    "options": [],
                    "answer": "retry",
                    "explanation": "An error occurred while generating the quiz."
                }
            ]
        }