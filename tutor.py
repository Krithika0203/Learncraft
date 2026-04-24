"""
tutor.py
AI Tutor chat powered by Groq. Maintains conversation history per session.
"""
from groq import Groq

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

SYSTEM_PROMPT = """You are LearnCraft Tutor — a friendly, encouraging, and highly knowledgeable AI tutor.
Your role is to help students understand topics deeply, answer their questions clearly, and guide them
step-by-step when they are confused.

Guidelines:
- Be concise but thorough. Use examples and analogies generously.
- If a student seems confused, break things down into smaller steps.
- Celebrate correct answers and effort warmly.
- Never just give answers to homework — guide the student to figure it out.
- Format responses with clear structure (use short paragraphs, numbered steps where helpful).
- Keep responses under 200 words unless a complex explanation is needed.
- Always end with a follow-up question or encouragement to keep the student engaged.
"""


def get_tutor_reply(messages: list, topic: str = "") -> str:
    """
    Send conversation history to Groq and return the tutor's reply.
    messages: list of {"role": "user"/"assistant", "content": str}
    """
    system = SYSTEM_PROMPT
    if topic:
        system += f"\n\nThe student is currently studying: {topic}. Focus your answers around this topic when relevant."

    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't connect right now. Please try again! (Error: {str(e)})"
