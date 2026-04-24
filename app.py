import time
import streamlit as st
import pandas as pd
from content_generator import generate_content
from quiz_generator import generate_quiz
from evaluation import evaluate_answers
from flashcard_generator import generate_flashcards
from tutor import get_tutor_reply
from pdf_export import export_study_notes_pdf, export_quiz_results_pdf
from gamification import (
    load_gamification, save_gamification,
    update_streak, award_xp, check_and_award_badges,
    get_level, get_xp_for_quiz, record_quiz,
    BADGES, XP_STUDY_SESSION, XP_FLASHCARD_DECK,
)
from utils import (
    get_topics, save_progress, load_progress,
    get_weak_topics, get_learning_path,
    load_notes, save_note, delete_note,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LearnCraft – Personalized Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Light Theme CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,700;0,900;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #f7f4ef;
    --surface:   #ffffff;
    --sidebar:   #1e1b4b;
    --accent:    #6c47ff;
    --accent2:   #f97316;
    --accent3:   #10b981;
    --text:      #1a1523;
    --muted:     #6b6880;
    --card:      #ffffff;
    --border:    #e2ddf5;
    --tag-bg:    #ede9fe;
    --tag-color: #6c47ff;
    --shadow:    0 2px 16px rgba(108,71,255,0.08);
    --shadow-lg: 0 8px 40px rgba(108,71,255,0.13);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #e2e0f5 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #fff !important; }

/* Headings */
h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: var(--text) !important;
    letter-spacing: -0.02em;
}

/* Cards */
.learn-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.6rem;
    margin: 0.75rem 0;
    box-shadow: var(--shadow);
    transition: transform 0.18s, box-shadow 0.18s;
}
.learn-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: var(--accent);
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #6c47ff 0%, #a78bfa 55%, #f97316 100%);
    border-radius: 24px;
    padding: 3.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hero::before {
    content: '';
    position: absolute; top:-60%; left:-30%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 55%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Fraunces', serif !important;
    font-size: 3.2rem !important;
    color: #fff !important;
    margin-bottom: 0.4rem !important;
    text-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.hero p { color: rgba(255,255,255,0.88) !important; font-size: 1.1rem; font-weight: 400; }

/* Tag pill */
.tag {
    display: inline-block;
    background: rgba(255,255,255,0.22);
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 100px;
    padding: 0.28rem 0.9rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Content blocks */
.content-block {
    background: var(--card);
    border-left: 4px solid var(--accent);
    border-radius: 0 14px 14px 0;
    padding: 1.5rem 2rem;
    margin: 0.9rem 0;
    box-shadow: var(--shadow);
    line-height: 1.8;
}
.content-block h3 {
    color: var(--accent) !important;
    font-size: 1.15rem !important;
    margin-bottom: 0.6rem !important;
}

/* Score badge */
.score-badge {
    font-size: 4.5rem;
    font-family: 'Fraunces', serif;
    font-weight: 900;
    background: linear-gradient(135deg, #6c47ff, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 99px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6c47ff, #8b6eff) !important;
    color: #fff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.62rem 2rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 4px 14px rgba(108,71,255,0.25) !important;
    transition: opacity 0.18s, transform 0.18s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* Inputs */
.stSelectbox > div > div,
.stTextInput > div > div,
.stTextArea > div > div,
.stNumberInput > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
}

/* Radio */
.stRadio > div { gap: 0.5rem; }
.stRadio label {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.1rem !important;
    transition: border-color 0.18s !important;
}
.stRadio label:hover { border-color: var(--accent) !important; }

/* Metrics */
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Fraunces', serif !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.82rem !important; }

/* Tabs */
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--accent) !important; }
.stTabs [data-baseweb="tab-border"] { background: var(--border) !important; }

/* Dividers */
hr { border-color: var(--border) !important; }

/* Alerts */
.stSuccess, .stWarning, .stError, .stInfo { border-radius: 12px !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 14px !important; overflow: hidden; box-shadow: var(--shadow); }

/* Flashcard flip */
.flip-card {
    perspective: 900px;
    height: 190px;
    cursor: pointer;
    margin: 0.5rem 0;
}
.flip-inner {
    position: relative; width: 100%; height: 100%;
    transition: transform 0.55s cubic-bezier(.4,2,.55,.44);
    transform-style: preserve-3d;
}
.flip-card.flipped .flip-inner { transform: rotateY(180deg); }
.flip-front, .flip-back {
    position: absolute; width: 100%; height: 100%;
    backface-visibility: hidden;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    padding: 1.2rem;
    text-align: center;
    box-shadow: var(--shadow);
}
.flip-front {
    background: var(--card);
    border: 2px solid var(--border);
    color: var(--text);
    font-weight: 600; font-size: 1rem;
}
.flip-back {
    background: linear-gradient(135deg, #6c47ff, #8b6eff);
    border: 2px solid transparent;
    color: #fff;
    font-size: 0.92rem;
    transform: rotateY(180deg);
}

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #e2e0f5 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    text-align: left !important;
    box-shadow: none !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.18) !important;
    transform: none !important;
}

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #6c47ff, #8b6eff);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    margin: 0.4rem 0 0.4rem 20%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 2px 8px rgba(108,71,255,0.18);
}
.chat-ai {
    background: #fff;
    color: #1a1523;
    border: 1.5px solid #e2ddf5;
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1.1rem;
    margin: 0.4rem 20% 0.4rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.chat-label { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.15rem; }
.badge-card { background:#fff; border:1.5px solid #e2ddf5; border-radius:14px; padding:1rem 0.8rem; text-align:center; box-shadow:0 2px 10px rgba(108,71,255,0.07); transition:transform 0.18s; }
.badge-card:hover { transform:translateY(-3px); }
.badge-card.earned { border-color:#6c47ff; background:#ede9fe; }
.badge-card.locked { opacity:0.45; filter:grayscale(0.6); }
.toast { background:linear-gradient(135deg,#6c47ff,#8b6eff); color:#fff; border-radius:14px; padding:0.9rem 1.3rem; margin:0.4rem 0; display:flex; align-items:center; gap:0.75rem; box-shadow:0 4px 18px rgba(108,71,255,0.25); }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "page": "home",
    "content": None,
    "quiz": None,
    "answers": {},
    "submitted": False,
    "progress": load_progress(),
    "quiz_start_time": None,
    "quiz_elapsed": None,
    "flashcards": [],
    "fc_index": 0,
    "fc_flipped": False,
    "daily_goal": 3,
    "sessions_today": 0,
    # Gamification
    "gami": load_gamification(),
    "new_badges": [],
    "xp_gained": 0,
    "level_up_msg": None,
    # Tutor chat
    "tutor_messages": [],
    "tutor_topic": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 2rem 0;'>
        <div style='font-size:2.4rem; margin-bottom:0.25rem;'>🎓</div>
        <div style='font-family: Fraunces, serif; font-size:1.5rem; font-weight:700; color:#fff;'>LearnCraft</div>
        <div style='color:rgba(226,224,245,0.6); font-size:0.82rem;'>Personalized Learning Platform</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home":            "home",
        "📚  Study Content":   "study",
        "🃏  Flashcards":      "flashcards",
        "🧩  Take Quiz":       "quiz",
        "🤖  AI Tutor":        "tutor",
        "🏅  Achievements":    "achievements",
        "📊  My Progress":     "progress",
        "📝  My Notes":        "notes",
    }
    for label, key in pages.items():
        is_active = st.session_state.page == key
        btn_label = f"▶  {label}" if is_active else label
        if st.button(btn_label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.submitted = False
            st.rerun()

    st.markdown("---")

    # XP & Level display
    gami = st.session_state.gami
    xp   = gami.get("xp", 0)
    streak = gami.get("streak", 0)
    level_name, next_level_name, xp_to_next, level_pct = get_level(xp)
    badges_earned = len(gami.get("badges", []))

    st.markdown(f"""
    <div style='margin-bottom:0.6rem;'>
        <div style='color:rgba(226,224,245,0.55); font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.3rem;'>Your Level</div>
        <div style='color:#fff; font-size:1.15rem; font-weight:700;'>{level_name}</div>
        <div style='color:#a78bfa; font-size:0.8rem; margin-top:0.1rem;'>{xp} XP {f"· {xp_to_next} to {next_level_name}" if next_level_name else "· MAX LEVEL"}</div>
        <div style='background:rgba(255,255,255,0.12); border-radius:99px; height:6px; margin-top:6px; overflow:hidden;'>
            <div style='height:100%; width:{level_pct}%; background:linear-gradient(90deg,#a78bfa,#f97316); border-radius:99px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Daily goal tracker
    progress = st.session_state.progress
    sessions_today = sum(
        1 for s in progress.get("sessions", [])
        if s.get("date") == str(__import__("datetime").date.today())
    )
    goal = st.session_state.daily_goal
    goal_pct = min(sessions_today / goal, 1.0)
    st.markdown(f"""
    <div style='margin-bottom:0.3rem;'>
        <div style='color:rgba(226,224,245,0.55); font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;'>Today's Goal</div>
        <div style='color:#fff; font-size:1.3rem; font-weight:700; margin:0.15rem 0;'>{sessions_today} / {goal} sessions</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(goal_pct)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    topics_count = len(set(progress.get("topics_studied", [])))
    best_score   = progress.get("best_score", 0)
    scores       = progress.get("scores", [])
    avg_score    = round(sum(scores)/len(scores), 1) if scores else 0

    st.markdown(f"""
    <div style='display:flex; gap:0.4rem; margin-top:0.5rem; flex-wrap:wrap;'>
        <div style='flex:1; min-width:48px; background:rgba(255,255,255,0.07); border-radius:10px; padding:0.5rem 0.4rem; text-align:center;'>
            <div style='font-size:1.1rem; font-weight:700; color:#f97316;'>🔥{streak}</div>
            <div style='font-size:0.63rem; color:rgba(226,224,245,0.55);'>Streak</div>
        </div>
        <div style='flex:1; min-width:48px; background:rgba(255,255,255,0.07); border-radius:10px; padding:0.5rem 0.4rem; text-align:center;'>
            <div style='font-size:1.1rem; font-weight:700; color:#a78bfa;'>{topics_count}</div>
            <div style='font-size:0.63rem; color:rgba(226,224,245,0.55);'>Topics</div>
        </div>
        <div style='flex:1; min-width:48px; background:rgba(255,255,255,0.07); border-radius:10px; padding:0.5rem 0.4rem; text-align:center;'>
            <div style='font-size:1.1rem; font-weight:700; color:#fbbf24;'>🏅{badges_earned}</div>
            <div style='font-size:0.63rem; color:rgba(226,224,245,0.55);'>Badges</div>
        </div>
        <div style='flex:1; min-width:48px; background:rgba(255,255,255,0.07); border-radius:10px; padding:0.5rem 0.4rem; text-align:center;'>
            <div style='font-size:1.1rem; font-weight:700; color:#10b981;'>{best_score}%</div>
            <div style='font-size:0.63rem; color:rgba(226,224,245,0.55);'>Best</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────────
page = st.session_state.page

# ══════════════════════ HOME ══════════════════════════════════════════════════
if page == "home":
    st.markdown("""
    <div class='hero'>
        <div class='tag'>AI-Powered Learning</div>
        <h1>LearnCraft</h1>
        <p>Generate personalized study material, flashcards & quizzes<br>tailored exactly to your level and learning goals.</p>
    </div>
    """, unsafe_allow_html=True)

    weak = get_weak_topics(st.session_state.progress)
    if weak:
        st.warning(f"📌 **Recommended Review:** You scored below 60% on: {', '.join(weak)}. Consider revisiting these topics!")

    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("📖", "Smart Content", "AI-generated study notes adapted to Beginner, Intermediate, or Advanced levels in multiple styles."),
        ("🃏", "Flashcards", "Flip-card revision sessions with auto-generated front/back cards. Perfect for memorisation."),
        ("🧩", "Custom Quizzes", "MCQ, True/False, Fill-in-the-Blank and Short Answer quizzes with timed mode."),
        ("📊", "Analytics", "Score history charts, per-topic bests, streak tracking and weak-topic detection."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
            <div class='learn-card'>
                <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
                <h3 style='font-size:1.1rem !important; margin-bottom:0.4rem;'>{title}</h3>
                <p style='color:#6b6880; font-size:0.87rem; line-height:1.6; margin:0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    qa, qb, qc = st.columns(3)
    with qa:
        if st.button("📚 Generate Study Notes", use_container_width=True):
            st.session_state.page = "study"; st.rerun()
    with qb:
        if st.button("🃏 Practice Flashcards", use_container_width=True):
            st.session_state.page = "flashcards"; st.rerun()
    with qc:
        if st.button("🧩 Start a Quiz", use_container_width=True):
            st.session_state.page = "quiz"; st.rerun()

    # Recent activity
    sessions = st.session_state.progress.get("sessions", [])
    if sessions:
        st.markdown("---")
        st.markdown("### 🕐 Recent Activity")
        recent = sessions[-5:][::-1]
        for s in recent:
            score = s.get("score", 0)
            color = "#10b981" if score >= 80 else "#f97316" if score >= 60 else "#ef4444"
            st.markdown(f"""
            <div style='background:#fff; border:1px solid #e2ddf5; border-radius:12px; padding:0.75rem 1.2rem; margin:0.3rem 0; display:flex; align-items:center; justify-content:space-between; box-shadow:0 2px 8px rgba(108,71,255,0.06);'>
                <div>
                    <span style='font-weight:600; color:#1a1523;'>{s.get("topic","Unknown")}</span>
                    <span style='color:#6b6880; font-size:0.82rem; margin-left:0.5rem;'>{s.get("date","")}</span>
                </div>
                <div style='font-weight:700; color:{color}; font-family:Fraunces,serif; font-size:1.1rem;'>{score}%</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════ STUDY ════════════════════════════════════════════════
elif page == "study":
    st.markdown("## 📚 Study Content Generator")
    st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Choose a topic and level to get personalized AI-generated study notes.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("📌 Topic", placeholder="e.g. Photosynthesis, World War II, Python Functions…")
        custom_focus = st.text_area("🎯 Focus area (optional)", placeholder="e.g. focus on the Calvin cycle, or key dates and battles…", height=75)
    with col2:
        level        = st.selectbox("🎓 Your Level",    ["Beginner", "Intermediate", "Advanced"])
        content_type = st.selectbox("📄 Content Style", ["Summary Notes", "Detailed Explanation", "Bullet Points", "Concept Map"])

    if topic:
        path = get_learning_path(topic)
        if path:
            path_html = " → ".join(
                f"<span style='color:#6c47ff; font-weight:700;'>{s}</span>" if s.lower() == topic.lower()
                else f"<span style='color:#6b6880;'>{s}</span>"
                for s in path
            )
            st.markdown(f"""
            <div style='background:#fff; border:1px solid #e2ddf5; border-radius:12px; padding:0.8rem 1.3rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(108,71,255,0.06);'>
                🗺️ <strong style='color:#1a1523;'>Suggested Path:</strong> &nbsp;{path_html}
            </div>
            """, unsafe_allow_html=True)

    if st.button("✨ Generate Content", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Crafting your personalized content…"):
                content = generate_content(topic, level, content_type, custom_focus)
                st.session_state.content = content
                save_progress(st.session_state.progress, topic=topic.title())
                # Gamification: award XP for study session
                gami = update_streak(st.session_state.gami)
                gami, xp_amt, lvl_up = award_xp(gami, XP_STUDY_SESSION, "study_session")
                topics_count = len(set(st.session_state.progress.get("topics_studied", [])))
                new_b = check_and_award_badges(gami, {"topics_count": topics_count, "event": ""})
                save_gamification(gami)
                st.session_state.gami = gami
                if new_b:
                    st.session_state.new_badges = new_b
                if lvl_up:
                    st.session_state.level_up_msg = lvl_up

    if st.session_state.content:
        st.markdown("---")
        data = st.session_state.content

        m1, m2, m3 = st.columns(3)
        m1.metric("Topic",          data["topic"])
        m2.metric("Level",          data["level"])
        m3.metric("Est. Read Time", data["read_time"])

        if data.get("ai_generated"):
            st.info("✨ Content is AI-generated and tailored to your topic and level.")

        for section in data["sections"]:
            st.markdown(f"""
            <div class='content-block'>
                <h3>📌 {section['title']}</h3>
                <div>{section['content']}</div>
            </div>
            """, unsafe_allow_html=True)

        if data.get("key_terms"):
            st.markdown("### 🔑 Key Terms")
            cols = st.columns(3)
            for i, term in enumerate(data["key_terms"]):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style='background:#f7f4ef; border:1px solid #e2ddf5; border-radius:10px; padding:0.7rem 1rem; margin:0.3rem 0;'>
                        <div style='color:#6c47ff; font-weight:700; font-size:0.9rem;'>{term['term']}</div>
                        <div style='color:#6b6880; font-size:0.82rem; margin-top:0.2rem;'>{term['definition']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        if data.get("summary"):
            st.markdown("### 💡 Quick Summary")
            st.info(data["summary"])

        st.markdown("---")
        col_note, col_quiz, col_flash = st.columns(3)
        with col_note:
            st.markdown("##### 📝 Save a Note")
            note_text = st.text_area("Note", placeholder="Something to remember…", height=75, label_visibility="collapsed")
            if st.button("💾 Save Note"):
                if note_text.strip():
                    save_note(note_text, data["topic"])
                    # Badge for first note
                    gami = st.session_state.gami
                    new_b = check_and_award_badges(gami, {"event": "note_saved"})
                    if new_b:
                        save_gamification(gami)
                        st.session_state.gami = gami
                        st.session_state.new_badges = new_b
                    st.success("Note saved!")
                else:
                    st.warning("Write something first.")
        with col_quiz:
            st.markdown("##### 🧩 Test Yourself")
            st.markdown("<div style='color:#6b6880; font-size:0.88rem; margin-bottom:0.6rem;'>Take a quiz on this exact topic.</div>", unsafe_allow_html=True)
            if st.button("🧩 Start Quiz on This Topic", use_container_width=True):
                st.session_state.page = "quiz"
                st.session_state.quiz_topic = data["topic"]
                st.session_state.quiz_level = data["level"]
                st.session_state.submitted = False
                st.rerun()
        with col_flash:
            st.markdown("##### 🃏 Flashcard Mode")
            st.markdown("<div style='color:#6b6880; font-size:0.88rem; margin-bottom:0.6rem;'>Generate flip-cards for quick revision.</div>", unsafe_allow_html=True)
            if st.button("🃏 Generate Flashcards", use_container_width=True):
                st.session_state.fc_topic = data["topic"]
                st.session_state.fc_level = data["level"]
                st.session_state.page = "flashcards"
                st.rerun()

        # PDF Export
        st.markdown("---")
        st.markdown("##### 📄 Export as PDF")
        if st.button("⬇️ Download Study Notes PDF", use_container_width=True):
            with st.spinner("Generating PDF…"):
                pdf_bytes = export_study_notes_pdf(data)
            st.download_button(
                label="📥 Click to Download PDF",
                data=pdf_bytes,
                file_name=f"LearnCraft_{data['topic'].replace(' ','_')}_Notes.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# ══════════════════════ FLASHCARDS ══════════════════════════════════════════
elif page == "flashcards":
    st.markdown("## 🃏 Flashcard Studio")
    st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Click any card to flip it and reveal the answer.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        default_topic = getattr(st.session_state, "fc_topic", "")
        fc_topic = st.text_input("📌 Topic", value=default_topic, placeholder="e.g. Quantum Mechanics, World War II…")
    with col2:
        default_level = getattr(st.session_state, "fc_level", "Intermediate")
        fc_level = st.selectbox("🎓 Level", ["Beginner", "Intermediate", "Advanced"],
                                index=["Beginner", "Intermediate", "Advanced"].index(default_level))
    num_cards = st.slider("Number of Cards", min_value=5, max_value=20, value=10)

    if st.button("🃏 Generate Flashcards", use_container_width=True):
        if not fc_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Creating your flashcard set…"):
                cards = generate_flashcards(fc_topic, fc_level, num_cards)
                st.session_state.flashcards = cards
                st.session_state.fc_index   = 0
                st.session_state.fc_flipped = False
                # Gamification: XP for flashcard deck
                gami = update_streak(st.session_state.gami)
                gami, xp_amt, lvl_up = award_xp(gami, XP_FLASHCARD_DECK, "flashcard_deck")
                new_b = check_and_award_badges(gami, {"event": "flashcards"})
                save_gamification(gami)
                st.session_state.gami = gami
                if new_b:
                    st.session_state.new_badges = new_b
                if lvl_up:
                    st.session_state.level_up_msg = lvl_up

    cards = st.session_state.flashcards
    if cards:
        st.markdown("---")
        idx = st.session_state.fc_index
        total_fc = len(cards)
        card = cards[idx]
        flipped = st.session_state.fc_flipped

        # Progress
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;'>
            <div style='color:#6b6880; font-size:0.88rem; font-weight:600;'>Card {idx+1} of {total_fc}</div>
            <div style='color:#6c47ff; font-size:0.88rem; font-weight:600;'>{round((idx+1)/total_fc*100)}% through deck</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress((idx + 1) / total_fc)

        # Flip card (CSS-based)
        flipped_class = "flipped" if flipped else ""
        st.markdown(f"""
        <div class="flip-card {flipped_class}" id="fc-main" onclick="this.classList.toggle('flipped')">
            <div class="flip-inner">
                <div class="flip-front">
                    <div>
                        <div style='font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#6b6880; margin-bottom:0.5rem;'>QUESTION</div>
                        <div style='font-size:1.05rem; font-weight:600; color:#1a1523;'>{card['front']}</div>
                    </div>
                </div>
                <div class="flip-back">
                    <div>
                        <div style='font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:rgba(255,255,255,0.7); margin-bottom:0.5rem;'>ANSWER</div>
                        <div style='font-size:0.95rem;'>{card['back']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("⬅ Previous", use_container_width=True, disabled=(idx == 0)):
                st.session_state.fc_index   = idx - 1
                st.session_state.fc_flipped = False
                st.rerun()
        with nav2:
            if st.button("🔄 Flip Card", use_container_width=True):
                st.session_state.fc_flipped = not st.session_state.fc_flipped
                st.rerun()
        with nav3:
            if st.button("Next ➡", use_container_width=True, disabled=(idx == total_fc - 1)):
                st.session_state.fc_index   = idx + 1
                st.session_state.fc_flipped = False
                st.rerun()

        # Mini deck overview
        st.markdown("---")
        st.markdown("### 📋 All Cards in This Deck")
        for i, c in enumerate(cards):
            bg = "#ede9fe" if i == idx else "#fff"
            bd = "#6c47ff" if i == idx else "#e2ddf5"
            st.markdown(f"""
            <div style='background:{bg}; border:1.5px solid {bd}; border-radius:10px; padding:0.6rem 1rem; margin:0.3rem 0; display:flex; justify-content:space-between;'>
                <div style='color:#1a1523; font-size:0.88rem; font-weight:600;'>{i+1}. {c['front']}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════ QUIZ ════════════════════════════════════════════════
elif page == "quiz":
    st.markdown("## 🧩 Quiz Generator")

    if not st.session_state.submitted:
        st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Configure your quiz, then test your knowledge!</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            default_topic = getattr(st.session_state, "quiz_topic", "")
            topic = st.text_input("📌 Topic", value=default_topic, placeholder="e.g. Machine Learning, Calculus…")
        with col2:
            default_level = getattr(st.session_state, "quiz_level", "Intermediate")
            level = st.selectbox("🎓 Difficulty", ["Beginner", "Intermediate", "Advanced"],
                                 index=["Beginner", "Intermediate", "Advanced"].index(default_level))

        col3, col4, col5 = st.columns(3)
        with col3:
            num_q      = st.number_input("Number of Questions", min_value=3, max_value=15, value=5)
        with col4:
            q_type     = st.selectbox("Question Type", ["Mixed", "Multiple Choice", "True/False", "Short Answer", "Fill in the Blank"])
        with col5:
            time_limit = st.selectbox("⏱️ Time Limit", ["No limit", "5 minutes", "10 minutes", "15 minutes"])

        if st.button("🎲 Generate Quiz", use_container_width=True):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                with st.spinner("Building your quiz…"):
                    quiz = generate_quiz(topic, level, num_q, q_type)
                    st.session_state.quiz            = quiz
                    st.session_state.answers         = {}
                    st.session_state.submitted       = False
                    st.session_state.quiz_start_time = time.time()
                    st.session_state.time_limit      = time_limit
                    st.session_state.quiz_elapsed    = None

        if st.session_state.quiz and not st.session_state.submitted:
            quiz = st.session_state.quiz

            if st.session_state.quiz_start_time:
                elapsed = int(time.time() - st.session_state.quiz_start_time)
                limit   = st.session_state.get("time_limit", "No limit")
                if limit != "No limit":
                    limit_secs = int(limit.split()[0]) * 60
                    remaining  = limit_secs - elapsed
                    if remaining <= 0:
                        st.error("⏱️ Time's up! Submitting…")
                        st.session_state.quiz_elapsed = elapsed
                        st.session_state.submitted    = True
                        st.rerun()
                    else:
                        r_m, r_s = divmod(remaining, 60)
                        st.info(f"⏱️ Time remaining: {r_m}m {r_s}s")
                else:
                    m, s = divmod(elapsed, 60)
                    st.info(f"⏱️ Elapsed: {m}m {s}s")

            st.markdown("---")
            st.markdown(f"### 📝 {quiz['title']}")
            st.markdown(f"<div style='color:#6b6880; margin-bottom:1.5rem;'>{len(quiz['questions'])} questions · {quiz['difficulty']} · {quiz['topic']}</div>", unsafe_allow_html=True)

            for i, q in enumerate(quiz["questions"]):
                st.markdown(f"""
                <div class='learn-card'>
                    <div style='color:#6b6880; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;'>Question {i+1} · {q['type']}</div>
                    <div style='font-size:1.02rem; font-weight:600; color:#1a1523; margin-bottom:1rem;'>{q['question']}</div>
                </div>
                """, unsafe_allow_html=True)

                if q["type"] in ("Multiple Choice", "True/False"):
                    ans = st.radio(f"Answer Q{i+1}", q["options"], key=f"q_{i}", label_visibility="collapsed")
                    st.session_state.answers[i] = ans
                elif q["type"] == "Fill in the Blank":
                    ans = st.text_input(f"Blank Q{i+1}", key=f"q_{i}", label_visibility="collapsed", placeholder="Type the missing word…")
                    st.session_state.answers[i] = ans
                else:
                    ans = st.text_input(f"Answer Q{i+1}", key=f"q_{i}", label_visibility="collapsed", placeholder="Type your answer…")
                    st.session_state.answers[i] = ans

            st.markdown("")
            if st.button("✅ Submit Quiz", use_container_width=True):
                st.session_state.quiz_elapsed = int(time.time() - st.session_state.quiz_start_time)
                st.session_state.submitted    = True
                st.rerun()

    else:
        # ── Results ──────────────────────────────────────────────────────────
        quiz    = st.session_state.quiz
        results = evaluate_answers(quiz, st.session_state.answers)
        score   = results["score_percent"]
        elapsed = st.session_state.get("quiz_elapsed", 0) or 0
        em, es  = divmod(elapsed, 60)

        st.markdown(f"""
        <div class='hero'>
            <div class='tag'>Quiz Complete</div>
            <div class='score-badge'>{score}%</div>
            <div style='color:rgba(255,255,255,0.85); margin-top:0.4rem;'>{results['correct']} / {results['total']} correct</div>
            <div style='color:rgba(255,255,255,0.7); font-size:0.9rem; margin-top:0.3rem;'>⏱️ Completed in {em}m {es}s</div>
            <div style='margin-top:1rem; font-size:1.1rem; color:#fff;'>{results['feedback']}</div>
        </div>
        """, unsafe_allow_html=True)

        save_progress(st.session_state.progress, score=score, topic=quiz["topic"])

        # Gamification: award XP for quiz
        gami = update_streak(st.session_state.gami)
        xp_for_quiz = get_xp_for_quiz(score)
        gami, xp_amt, lvl_up = award_xp(gami, xp_for_quiz)
        gami = record_quiz(gami, score, len(set(st.session_state.progress.get("topics_studied", []))))
        topics_count  = len(set(st.session_state.progress.get("topics_studied", [])))
        quizzes_count = gami.get("total_quizzes", 0)
        new_b = check_and_award_badges(gami, {
            "score": score, "topics_count": topics_count,
            "quizzes_count": quizzes_count, "event": "quiz",
        })
        save_gamification(gami)
        st.session_state.gami = gami
        if new_b:
            st.session_state.new_badges = new_b
        if lvl_up:
            st.session_state.level_up_msg = lvl_up

        # Show XP toast
        st.markdown(f"""
        <div class='toast'>
            <div style='font-size:1.5rem;'>⚡</div>
            <div>
                <div style='font-weight:700; font-size:0.95rem;'>+{xp_for_quiz} XP earned!</div>
                <div style='font-size:0.82rem; opacity:0.85;'>Total: {gami.get("xp",0)} XP · {get_level(gami.get("xp",0))[0]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show new badges
        if st.session_state.new_badges:
            for bk in st.session_state.new_badges:
                b = BADGES.get(bk, {})
                st.markdown(f"""
                <div class='toast' style='background:linear-gradient(135deg,#f97316,#fbbf24);'>
                    <div style='font-size:1.5rem;'>{b.get("icon","🏅")}</div>
                    <div>
                        <div style='font-weight:700; font-size:0.95rem;'>Badge Unlocked: {b.get("name","")}</div>
                        <div style='font-size:0.82rem; opacity:0.85;'>{b.get("desc","")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.session_state.new_badges = []

        if lvl_up:
            st.balloons()
            st.success(f"🚀 Level Up! You reached **{lvl_up}**!")
            st.session_state.level_up_msg = None

        if score < 60:
            st.warning(f"📌 Score below 60%. We recommend revisiting **{quiz['topic']}**.")

        # Score meter
        col_meter = st.columns([1, 2, 1])[1]
        with col_meter:
            level_label = "Excellent 🌟" if score == 100 else "Great 🎉" if score >= 80 else "Good 👍" if score >= 60 else "Fair 📖" if score >= 40 else "Keep Going 💪"
            st.markdown(f"<div style='text-align:center; color:#6c47ff; font-weight:700; margin-bottom:0.3rem;'>{level_label}</div>", unsafe_allow_html=True)
            st.progress(score / 100)

        st.markdown("### 📋 Answer Review")
        for i, q in enumerate(quiz["questions"]):
            correct = results["details"][i]["correct"]
            user_ans = st.session_state.answers.get(i, "")
            color  = "#10b981" if correct else "#ef4444"
            icon   = "✅" if correct else "❌"
            st.markdown(f"""
            <div style='background:#fff; border:1px solid {color}33; border-left:4px solid {color}; border-radius:0 14px 14px 0; padding:1.2rem 1.5rem; margin:0.6rem 0; box-shadow:0 2px 8px rgba(0,0,0,0.04);'>
                <div style='font-weight:700; margin-bottom:0.5rem; color:#1a1523;'>{icon} Q{i+1}: {q['question']}</div>
                <div style='font-size:0.88rem; color:#6b6880;'>Your answer: <span style='color:{color}; font-weight:600;'>{user_ans if user_ans else "No answer"}</span></div>
                <div style='font-size:0.88rem; color:#6b6880;'>Correct: <span style='color:#10b981; font-weight:600;'>{results["details"][i]["correct_answer"]}</span></div>
                {f'<div style="font-size:0.82rem; color:#6b6880; margin-top:0.35rem; font-style:italic;">{results["details"][i]["explanation"]}</div>' if results["details"][i].get("explanation") else ""}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔁 Retake Quiz", use_container_width=True):
                st.session_state.submitted       = False
                st.session_state.answers         = {}
                st.session_state.quiz_start_time = time.time()
                st.rerun()
        with c2:
            if st.button("📚 Study This Topic", use_container_width=True):
                st.session_state.page      = "study"
                st.session_state.submitted = False
                st.rerun()
        with c3:
            if st.button("🃏 Flashcard Revision", use_container_width=True):
                st.session_state.fc_topic = quiz["topic"]
                st.session_state.fc_level = quiz["difficulty"]
                st.session_state.page     = "flashcards"
                st.session_state.submitted = False
                st.rerun()

        # PDF Export for quiz results
        st.markdown("---")
        if st.button("⬇️ Download Quiz Results PDF", use_container_width=True):
            with st.spinner("Generating PDF…"):
                pdf_bytes = export_quiz_results_pdf(quiz, results, st.session_state.answers)
            st.download_button(
                label="📥 Click to Download Results PDF",
                data=pdf_bytes,
                file_name=f"LearnCraft_{quiz['topic'].replace(' ','_')}_Results.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# ══════════════════════ PROGRESS ════════════════════════════════════════════
elif page == "progress":
    st.markdown("## 📊 My Learning Progress")
    progress = st.session_state.progress
    scores   = progress.get("scores", [])
    sessions = progress.get("sessions", [])

    c1, c2, c3, c4 = st.columns(4)
    topics_list = list(set(progress.get("topics_studied", [])))
    avg = round(sum(scores)/len(scores), 1) if scores else 0
    c1.metric("📚 Topics Studied",  len(topics_list))
    c2.metric("🏆 Best Score",      f"{progress.get('best_score', 0)}%")
    c3.metric("📈 Avg Score",       f"{avg}%")
    c4.metric("🎯 Total Quizzes",   len(scores))

    st.markdown("---")

    if sessions:
        st.markdown("### 📈 Score History")
        df = pd.DataFrame(sessions)
        df.index = range(1, len(df) + 1)
        df.index.name = "Quiz #"
        st.line_chart(df[["score"]].rename(columns={"score": "Score (%)"}), color="#6c47ff")

    topic_scores = progress.get("topic_scores", {})
    if topic_scores:
        st.markdown("### 🏅 Best Score Per Topic")
        ts_df = pd.DataFrame([
            {"Topic": t, "Best Score (%)": s, "Status": "✅ Passing" if s >= 60 else "⚠️ Needs Review"}
            for t, s in sorted(topic_scores.items(), key=lambda x: -x[1])
        ])
        st.dataframe(ts_df, use_container_width=True, hide_index=True)

    weak = get_weak_topics(progress)
    if weak:
        st.markdown("### ⚠️ Topics to Improve")
        for t in weak:
            st.markdown(f"""
            <div style='background:#fff; border:1px solid #ef444433; border-left:4px solid #ef4444; border-radius:0 12px 12px 0; padding:0.65rem 1.1rem; margin:0.35rem 0; color:#ef4444; font-weight:600;'>
                ⚠️ {t} — below 60%
            </div>
            """, unsafe_allow_html=True)

    if topics_list:
        st.markdown("### 🗂️ Topics Covered")
        cols = st.columns(3)
        for i, t in enumerate(topics_list):
            with cols[i % 3]:
                best = topic_scores.get(t, 0)
                color = "#10b981" if best >= 80 else "#f97316" if best >= 60 else "#ef4444"
                st.markdown(f"""
                <div style='background:#fff; border:1px solid #e2ddf5; border-radius:10px; padding:0.7rem 1rem; margin:0.3rem 0; display:flex; justify-content:space-between; align-items:center;'>
                    <div style='color:#1a1523; font-weight:600; font-size:0.9rem;'>📌 {t}</div>
                    <div style='color:{color}; font-weight:700; font-size:0.9rem;'>{best}%</div>
                </div>
                """, unsafe_allow_html=True)

    if not topics_list and not scores:
        st.markdown("""
        <div style='text-align:center; padding:4rem 2rem; color:#6b6880;'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🌱</div>
            <div style='font-size:1.2rem;'>No activity yet. Start learning to see your progress!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📚 Start Learning Now", use_container_width=True):
            st.session_state.page = "study"; st.rerun()

    st.markdown("")
    if st.button("🗑️ Reset All Progress", type="secondary"):
        st.session_state.progress = {"topics_studied": [], "scores": [], "best_score": 0, "sessions": [], "topic_scores": {}}
        save_progress(st.session_state.progress)
        st.success("Progress reset.")
        st.rerun()

# ══════════════════════ NOTES ═══════════════════════════════════════════════
elif page == "notes":
    st.markdown("## 📝 My Notes")
    st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Notes you've saved while studying.</div>", unsafe_allow_html=True)

    notes = load_notes()

    if not notes:
        st.markdown("""
        <div style='text-align:center; padding:4rem 2rem; color:#6b6880;'>
            <div style='font-size:3rem; margin-bottom:1rem;'>📭</div>
            <div style='font-size:1.2rem;'>No notes yet. Save notes from the Study page!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📚 Go to Study", use_container_width=True):
            st.session_state.page = "study"; st.rerun()
    else:
        # Search filter
        search = st.text_input("🔍 Search notes", placeholder="Filter by keyword…")
        filtered = [n for n in reversed(notes) if not search or search.lower() in n.get("note","").lower() or search.lower() in n.get("topic","").lower()]
        st.markdown(f"**{len(filtered)} note(s)**")

        for i, note in enumerate(filtered):
            actual_index = notes.index(note) if note in notes else -1
            col_note, col_del = st.columns([11, 1])
            with col_note:
                st.markdown(f"""
                <div style='background:#fff; border:1px solid #e2ddf5; border-left:4px solid #6c47ff; border-radius:0 14px 14px 0; padding:1rem 1.5rem; margin:0.5rem 0; box-shadow:0 2px 8px rgba(108,71,255,0.06);'>
                    <div style='color:#6c47ff; font-size:0.78rem; font-weight:700; margin-bottom:0.4rem;'>📌 {note.get("topic","Unknown")} · {note.get("date","")}</div>
                    <div style='color:#1a1523; font-size:0.95rem; line-height:1.65;'>{note.get("note","")}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{i}", help="Delete note"):
                    if actual_index >= 0:
                        delete_note(actual_index)
                        st.rerun()

# ══════════════════════ AI TUTOR ═════════════════════════════════════════════
elif page == "tutor":
    st.markdown("## 🤖 AI Tutor")
    st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Ask anything about any topic. Your tutor remembers the full conversation.</div>", unsafe_allow_html=True)

    # Topic context selector
    col_t, col_c = st.columns([3, 1])
    with col_t:
        tutor_topic = st.text_input(
            "📌 Topic context (optional)",
            value=st.session_state.tutor_topic,
            placeholder="e.g. Quantum Mechanics — helps the tutor stay focused",
        )
        st.session_state.tutor_topic = tutor_topic
    with col_c:
        st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.tutor_messages = []
            st.rerun()

    st.markdown("---")

    # Render conversation history
    msgs = st.session_state.tutor_messages
    if not msgs:
        st.markdown("""
        <div style='text-align:center; padding:3rem 2rem; color:#6b6880;'>
            <div style='font-size:3rem; margin-bottom:0.75rem;'>🤖</div>
            <div style='font-size:1.1rem; font-weight:600; color:#1a1523; margin-bottom:0.4rem;'>Hi! I'm your LearnCraft Tutor.</div>
            <div style='font-size:0.95rem;'>Ask me anything about your topic — concepts, examples, quick tests, or explanations.</div>
        </div>
        """, unsafe_allow_html=True)

        # Quick-start prompts
        st.markdown("#### 💡 Try asking:")
        prompts = [
            "Explain this topic like I'm 10 years old",
            "Give me 3 real-world examples",
            "What are the most common mistakes beginners make?",
            "Quiz me with one question",
        ]
        p_cols = st.columns(2)
        for i, prompt in enumerate(prompts):
            with p_cols[i % 2]:
                if st.button(f'"{prompt}"', key=f"prompt_{i}", use_container_width=True):
                    full_prompt = prompt + (f" about {tutor_topic}" if tutor_topic else "")
                    st.session_state.tutor_messages.append({"role": "user", "content": full_prompt})
                    with st.spinner("Thinking…"):
                        reply = get_tutor_reply(st.session_state.tutor_messages, tutor_topic)
                    st.session_state.tutor_messages.append({"role": "assistant", "content": reply})
                    st.rerun()
    else:
        for msg in msgs:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='text-align:right; margin-bottom:0.15rem;'>
                    <span style='font-size:0.72rem; font-weight:700; color:#6b6880; text-transform:uppercase; letter-spacing:0.05em;'>You</span>
                </div>
                <div class='chat-user'>{msg['content']}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='margin-bottom:0.15rem;'>
                    <span style='font-size:0.72rem; font-weight:700; color:#6c47ff; text-transform:uppercase; letter-spacing:0.05em;'>🤖 Tutor</span>
                </div>
                <div class='chat-ai'>{msg['content']}</div>
                """, unsafe_allow_html=True)

    # Input box
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your question",
            placeholder="Ask your tutor anything…",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send ➤", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.tutor_messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Tutor is thinking…"):
            reply = get_tutor_reply(st.session_state.tutor_messages, tutor_topic)
        st.session_state.tutor_messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ══════════════════════ ACHIEVEMENTS ════════════════════════════════════════
elif page == "achievements":
    gami   = st.session_state.gami
    xp     = gami.get("xp", 0)
    streak = gami.get("streak", 0)
    earned = set(gami.get("badges", []))
    level_name, next_level_name, xp_to_next, level_pct = get_level(xp)

    st.markdown("## 🏅 Achievements")
    st.markdown("<div style='color:#6b6880; margin-bottom:1rem;'>Your XP, level, streak and badges.</div>", unsafe_allow_html=True)

    # XP / Level hero card
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#6c47ff,#a78bfa,#f97316); border-radius:22px; padding:2.5rem 2rem; text-align:center; margin-bottom:1.5rem; box-shadow:0 8px 40px rgba(108,71,255,0.18);'>
        <div style='font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:rgba(255,255,255,0.7); margin-bottom:0.5rem;'>Current Level</div>
        <div style='font-family:Fraunces,serif; font-size:2.8rem; font-weight:900; color:#fff; margin-bottom:0.2rem;'>{level_name}</div>
        <div style='color:rgba(255,255,255,0.85); font-size:1.1rem; font-weight:600;'>{xp} XP total</div>
        {"<div style='color:rgba(255,255,255,0.65); font-size:0.88rem; margin-top:0.3rem;'>" + str(xp_to_next) + " XP to " + str(next_level_name) + "</div>" if next_level_name else "<div style='color:rgba(255,255,255,0.65); font-size:0.88rem; margin-top:0.3rem;'>Maximum level reached! 🚀</div>"}
        <div style='background:rgba(255,255,255,0.2); border-radius:99px; height:8px; margin:1rem auto 0; max-width:320px; overflow:hidden;'>
            <div style='height:100%; width:{level_pct}%; background:#fff; border-radius:99px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    total_quizzes = gami.get("total_quizzes", 0)
    badges_count  = len(earned)
    s1, s2, s3, s4 = st.columns(4)
    for col, icon, val, label in [
        (s1, "🔥", f"{streak} days", "Current Streak"),
        (s2, "⚡", f"{xp} XP",       "Total XP"),
        (s3, "🧩", str(total_quizzes), "Quizzes Done"),
        (s4, "🏅", f"{badges_count}/{len(BADGES)}", "Badges Earned"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#fff; border:1.5px solid #e2ddf5; border-radius:16px; padding:1.2rem 0.8rem; text-align:center; box-shadow:0 2px 10px rgba(108,71,255,0.07);'>
                <div style='font-size:1.6rem; margin-bottom:0.3rem;'>{icon}</div>
                <div style='font-family:Fraunces,serif; font-size:1.4rem; font-weight:700; color:#1a1523;'>{val}</div>
                <div style='font-size:0.75rem; color:#6b6880; font-weight:600;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏅 Badge Collection")

    # Filter tabs
    filter_tab1, filter_tab2 = st.tabs(["All Badges", "Earned Only"])

    def render_badges(badge_list):
        cols = st.columns(4)
        for i, (key, badge) in enumerate(badge_list):
            is_earned = key in earned
            card_class = "badge-card earned" if is_earned else "badge-card locked"
            lock_icon  = badge["icon"] if is_earned else "🔒"
            opacity    = "1" if is_earned else "0.5"
            with cols[i % 4]:
                st.markdown(f"""
                <div class='{card_class}' style='opacity:{opacity};'>
                    <div style='font-size:2rem; margin-bottom:0.4rem;'>{lock_icon}</div>
                    <div style='font-weight:700; font-size:0.88rem; color:#1a1523; margin-bottom:0.2rem;'>{badge["name"]}</div>
                    <div style='font-size:0.76rem; color:#6b6880; line-height:1.4;'>{badge["desc"]}</div>
                    {"<div style='margin-top:0.4rem; font-size:0.7rem; font-weight:700; color:#6c47ff; text-transform:uppercase; letter-spacing:0.05em;'>✓ Earned</div>" if is_earned else ""}
                </div>
                """, unsafe_allow_html=True)

    with filter_tab1:
        render_badges(list(BADGES.items()))
    with filter_tab2:
        earned_list = [(k, v) for k, v in BADGES.items() if k in earned]
        if earned_list:
            render_badges(earned_list)
        else:
            st.markdown("""
            <div style='text-align:center; padding:3rem; color:#6b6880;'>
                <div style='font-size:2.5rem; margin-bottom:0.75rem;'>🔒</div>
                <div>No badges yet — complete quizzes and study sessions to earn them!</div>
            </div>
            """, unsafe_allow_html=True)

    # How to earn XP guide
    st.markdown("---")
    st.markdown("### ⚡ How to Earn XP")
    xp_guide = [
        ("📚", "Study session",     "+10 XP"),
        ("🃏", "Flashcard deck",    "+10 XP"),
        ("🧩", "Complete a quiz",   "+20 XP"),
        ("🎯", "Score ≥ 60%",       "+15 XP"),
        ("🎉", "Score ≥ 80%",       "+30 XP"),
        ("💯", "Perfect score 100%","+50 XP"),
    ]
    xp_cols = st.columns(3)
    for i, (icon, action, xp_val) in enumerate(xp_guide):
        with xp_cols[i % 3]:
            st.markdown(f"""
            <div style='background:#fff; border:1px solid #e2ddf5; border-radius:12px; padding:0.8rem 1rem; margin:0.3rem 0; display:flex; justify-content:space-between; align-items:center; box-shadow:0 1px 6px rgba(108,71,255,0.05);'>
                <div style='font-size:0.9rem; color:#1a1523;'>{icon} {action}</div>
                <div style='font-weight:700; color:#6c47ff; font-size:0.9rem;'>{xp_val}</div>
            </div>
            """, unsafe_allow_html=True)
