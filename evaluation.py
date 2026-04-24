"""
evaluation.py
Evaluates quiz answers and returns detailed results.
Supports Multiple Choice, True/False, Short Answer, Fill in the Blank.
"""


def evaluate_answers(quiz: dict, answers: dict) -> dict:
    questions = quiz["questions"]
    total = len(questions)
    correct_count = 0
    details = []

    for i, q in enumerate(questions):
        user_ans = str(answers.get(i, "")).strip().lower()
        correct_ans = str(q.get("answer", "")).strip().lower()
        q_type = q.get("type", "")

        if q_type in ("Short Answer", "Fill in the Blank"):
            # Accept if either string contains the other
            is_correct = correct_ans in user_ans or user_ans in correct_ans
        else:
            is_correct = user_ans == correct_ans

        if is_correct:
            correct_count += 1

        details.append({
            "correct": is_correct,
            "correct_answer": q.get("answer", "N/A"),
            "explanation": q.get("explanation", ""),
        })

    score_pct = round((correct_count / total) * 100) if total > 0 else 0

    if score_pct == 100:
        feedback = "🌟 Perfect score! Outstanding work!"
    elif score_pct >= 80:
        feedback = "🎉 Excellent! You have a strong grasp of the material."
    elif score_pct >= 60:
        feedback = "👍 Good effort! Review the questions you missed to reinforce your understanding."
    elif score_pct >= 40:
        feedback = "📖 Keep practising. Revisit the study material for the topics you found tricky."
    else:
        feedback = "💪 Don't give up! Go back to the study notes and try again — you'll improve."

    return {
        "score_percent": score_pct,
        "correct": correct_count,
        "total": total,
        "feedback": feedback,
        "details": details,
    }