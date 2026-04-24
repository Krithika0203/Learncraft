"""
pdf_export.py
Generates formatted PDF exports for study notes and quiz results using reportlab.
"""
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── Brand colours ─────────────────────────────────────────────────────────────
PURPLE = colors.HexColor("#6c47ff")
ORANGE = colors.HexColor("#f97316")
LIGHT  = colors.HexColor("#f7f4ef")
MUTED  = colors.HexColor("#6b6880")
DARK   = colors.HexColor("#1a1523")
WHITE  = colors.white
GREEN  = colors.HexColor("#10b981")
RED    = colors.HexColor("#ef4444")


def _base_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title2", parent=base["Title"],
            fontSize=26, textColor=PURPLE, spaceAfter=4,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"],
            fontSize=11, textColor=MUTED, spaceAfter=16,
            fontName="Helvetica", alignment=TA_CENTER,
        ),
        "section_head": ParagraphStyle(
            "SectionHead", parent=base["Heading2"],
            fontSize=13, textColor=PURPLE, spaceBefore=14, spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body2", parent=base["Normal"],
            fontSize=10, textColor=DARK, spaceAfter=6,
            fontName="Helvetica", leading=15,
        ),
        "term": ParagraphStyle(
            "Term", parent=base["Normal"],
            fontSize=10, textColor=PURPLE, spaceAfter=2,
            fontName="Helvetica-Bold",
        ),
        "definition": ParagraphStyle(
            "Def", parent=base["Normal"],
            fontSize=9.5, textColor=MUTED, spaceAfter=8,
            fontName="Helvetica", leading=14,
        ),
        "summary_box": ParagraphStyle(
            "SummaryBox", parent=base["Normal"],
            fontSize=10, textColor=DARK, spaceAfter=6,
            fontName="Helvetica-Oblique", leading=15,
        ),
        "label": ParagraphStyle(
            "Label", parent=base["Normal"],
            fontSize=8, textColor=MUTED, spaceAfter=2,
            fontName="Helvetica", alignment=TA_CENTER,
        ),
        "score_big": ParagraphStyle(
            "ScoreBig", parent=base["Normal"],
            fontSize=40, textColor=PURPLE, spaceAfter=4,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
        ),
        "feedback": ParagraphStyle(
            "Feedback", parent=base["Normal"],
            fontSize=12, textColor=DARK, spaceAfter=12,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
        ),
        "q_text": ParagraphStyle(
            "QText", parent=base["Normal"],
            fontSize=10, textColor=DARK, spaceAfter=3,
            fontName="Helvetica-Bold",
        ),
        "q_detail": ParagraphStyle(
            "QDetail", parent=base["Normal"],
            fontSize=9.5, textColor=MUTED, spaceAfter=2,
            fontName="Helvetica",
        ),
    }
    return styles


def export_study_notes_pdf(content: dict) -> bytes:
    """Generate a PDF for study notes. Returns bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )
    s = _base_styles()
    story = []

    # Header
    story.append(Paragraph("LearnCraft", s["title"]))
    story.append(Paragraph("Personalized Study Notes", s["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=12))

    # Meta table
    meta_data = [
        ["Topic", content.get("topic", "—"), "Level", content.get("level", "—")],
        ["Style", content.get("style", "—"), "Read Time", content.get("read_time", "—")],
        ["Generated", str(date.today()), "", ""],
    ]
    meta_table = Table(meta_data, colWidths=[30*mm, 65*mm, 30*mm, 50*mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",   (0,0), (0,-1), PURPLE),
        ("TEXTCOLOR",   (2,0), (2,-1), PURPLE),
        ("TEXTCOLOR",   (1,0), (1,-1), DARK),
        ("TEXTCOLOR",   (3,0), (3,-1), DARK),
        ("BACKGROUND",  (0,0), (-1,-1), LIGHT),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT, WHITE]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#e2ddf5")),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Sections
    for section in content.get("sections", []):
        story.append(Paragraph(f"▸  {section['title']}", s["section_head"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2ddf5"), spaceAfter=6))
        story.append(Paragraph(section["content"], s["body"]))

    # Key terms
    key_terms = content.get("key_terms", [])
    if key_terms:
        story.append(Spacer(1, 6))
        story.append(Paragraph("Key Terms", s["section_head"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2ddf5"), spaceAfter=8))
        for term in key_terms:
            story.append(Paragraph(term["term"], s["term"]))
            story.append(Paragraph(term["definition"], s["definition"]))

    # Summary
    summary = content.get("summary", "")
    if summary:
        story.append(Spacer(1, 4))
        story.append(Paragraph("Quick Summary", s["section_head"]))
        summary_table = Table([[Paragraph(f'"{summary}"', s["summary_box"])]], colWidths=[170*mm])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#ede9fe")),
            ("LEFTPADDING",  (0,0), (-1,-1), 12),
            ("RIGHTPADDING", (0,0), (-1,-1), 12),
            ("TOPPADDING",   (0,0), (-1,-1), 10),
            ("BOTTOMPADDING",(0,0), (-1,-1), 10),
            ("ROUNDEDCORNERS", [8]),
        ]))
        story.append(summary_table)

    # Footer
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2ddf5"), spaceAfter=6))
    story.append(Paragraph(f"Generated by LearnCraft · {date.today()}", s["label"]))

    doc.build(story)
    return buffer.getvalue()


def export_quiz_results_pdf(quiz: dict, results: dict, answers: dict) -> bytes:
    """Generate a PDF for quiz results. Returns bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )
    s = _base_styles()
    story = []

    # Header
    story.append(Paragraph("LearnCraft", s["title"]))
    story.append(Paragraph("Quiz Results Report", s["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=14))

    # Score hero
    score     = results["score_percent"]
    score_col = GREEN if score >= 60 else RED
    story.append(Paragraph(f"{score}%", ParagraphStyle(
        "BigScore", fontSize=48, textColor=score_col,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4,
    )))
    story.append(Paragraph(
        f"{results['correct']} / {results['total']} correct  ·  {results['feedback']}",
        s["feedback"]
    ))
    story.append(Spacer(1, 6))

    # Meta
    meta_data = [
        ["Topic",      quiz.get("topic", "—"),      "Difficulty", quiz.get("difficulty", "—")],
        ["Questions",  str(results["total"]),         "Date",       str(date.today())],
    ]
    meta_table = Table(meta_data, colWidths=[30*mm, 65*mm, 30*mm, 50*mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",   (0,0), (0,-1), PURPLE),
        ("TEXTCOLOR",   (2,0), (2,-1), PURPLE),
        ("BACKGROUND",  (0,0), (-1,-1), LIGHT),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT, WHITE]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#e2ddf5")),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Answer review
    story.append(Paragraph("Answer Review", s["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2ddf5"), spaceAfter=8))

    for i, q in enumerate(quiz.get("questions", [])):
        correct    = results["details"][i]["correct"]
        user_ans   = str(answers.get(i, "No answer"))
        right_ans  = results["details"][i]["correct_answer"]
        explanation= results["details"][i].get("explanation", "")
        icon       = "✓" if correct else "✗"
        bg_color   = colors.HexColor("#d1fae5") if correct else colors.HexColor("#fee2e2")
        icon_color = GREEN if correct else RED

        block = [
            [
                Paragraph(f"<font color='{'#10b981' if correct else '#ef4444'}'><b>{icon}</b></font>  Q{i+1}: {q['question']}", s["q_text"]),
            ],
            [
                Paragraph(
                    f"Your answer: <font color='{'#10b981' if correct else '#ef4444'}'><b>{user_ans}</b></font>   |   "
                    f"Correct: <font color='#10b981'><b>{right_ans}</b></font>"
                    + (f"<br/><i>{explanation}</i>" if explanation else ""),
                    s["q_detail"]
                ),
            ],
        ]
        t = Table(block, colWidths=[170*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), bg_color),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 10),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("ROUNDEDCORNERS", [6]),
        ]))
        story.append(KeepTogether([t, Spacer(1, 5)]))

    # Footer
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2ddf5"), spaceAfter=6))
    story.append(Paragraph(f"Generated by LearnCraft · {date.today()}", s["label"]))

    doc.build(story)
    return buffer.getvalue()
