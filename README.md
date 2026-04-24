<div align="center">

<br>

```
██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗ ██████╗██████╗  █████╗ ███████╗████████╗
██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██║     █████╗  ███████║██████╔╝██╔██╗ ██║██║     ██████╔╝███████║█████╗     ██║   
██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║██║     ██╔══██╗██╔══██║██╔══╝     ██║   
███████╗███████╗██║  ██║██║  ██║██║ ╚████║╚██████╗██║  ██║██║  ██║██║        ██║   
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
```

### 🎓 Personalized AI Learning Platform

*Generate notes · flashcards · quizzes · and chat with an AI tutor — all tailored to your level.*

<br>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA--3.3--70b-F97316?style=for-the-badge&logoColor=white)](https://console.groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-FFD21E?style=for-the-badge)](https://huggingface.co/spaces)

<br>

</div>

---

## 🌟 Overview

**LearnCraft** is a fully AI-powered learning platform that generates **customized study content** based on your chosen topic and difficulty level. Whether you're a beginner learning Python or an advanced student tackling Quantum Mechanics — LearnCraft adapts everything to *you*.

```
Pick a topic  →  Choose your level  →  Get personalized content  →  Track your progress
```

---

## ✨ Features

| Module | What it does |
|---|---|
| 📚 **Study Content Generator** | AI-generated notes in 4 styles: Summary, Detailed, Bullet Points, Concept Map |
| 🃏 **Flashcard Studio** | Auto-generated flip-card decks (up to 20 cards) for any topic |
| 🧩 **Quiz Engine** | MCQ, True/False, Fill-in-the-Blank, Short Answer — with optional timed mode |
| 🤖 **AI Tutor Chat** | Multi-turn conversational tutor with topic context and full conversation memory |
| 🏅 **Gamification** | XP points, 7 levels, 15 badges, daily streak tracking |
| 📄 **PDF Export** | Download study notes and quiz results as branded A4 PDFs |
| 📊 **Progress Dashboard** | Score history chart, per-topic best scores, weak topic detection |
| 📝 **My Notes** | Save, search and delete personal notes during study sessions |

---

## 🚀 Getting Started

### Option 1 — Run on Hugging Face Spaces *(recommended)*

1. Fork this Space on Hugging Face
2. Go to **Settings → Repository secrets**
3. Add your Groq API key:

```
Name:  GROQ_API_KEY
Value: gsk_your_key_here
```

> 🔑 Get a **free** Groq API key at [console.groq.com](https://console.groq.com) — takes under a minute.

### Option 2 — Run locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/learncraft.git
cd learncraft

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export GROQ_API_KEY="gsk_your_key_here"    # macOS/Linux
# set GROQ_API_KEY=gsk_your_key_here       # Windows

# 4. Launch
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
groq>=0.4.0
reportlab>=4.0.0
plotly>=5.18.0
```

---

## 📂 Project Structure

```
learncraft/
├── app.py                   # Streamlit routing, session state, UI
├── content_generator.py     # AI study note generation
├── quiz_generator.py        # Quiz creation & question formatting
├── flashcard_generator.py   # Flashcard deck generation
├── tutor.py                 # Multi-turn AI tutor chat
├── evaluation.py            # Quiz answer scoring logic
├── gamification.py          # XP, badges, streak tracking
├── pdf_export.py            # ReportLab PDF generation
├── utils.py                 # JSON persistence helpers
├── requirements.txt
└── README.md
```

**Data files (auto-created at runtime):**
```
learning_progress.json       # Quiz scores & topic history
notes.json                   # Saved user notes
gamification.json            # XP, badges, streaks
```

---

## 🗺️ App Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Hero banner, feature overview, quick-start buttons, activity feed |
| 📚 **Study Content** | Generate AI notes with key terms, summary and PDF export |
| 🃏 **Flashcards** | Navigate flip cards with progress bar and deck overview |
| 🧩 **Take Quiz** | Timed quiz with instant results, XP awards, PDF download |
| 🤖 **AI Tutor** | Chat with an AI tutor — quick-start prompts and topic context |
| 🏅 **Achievements** | XP level card, badge gallery, streak stats |
| 📊 **My Progress** | Score history, per-topic performance table, weak topic alerts |
| 📝 **My Notes** | Searchable saved notes from study sessions |

---

## 🏅 Gamification System

### XP Actions

| Action | XP Earned |
|---|---|
| Generate study notes | +10 XP |
| Complete a flashcard deck | +10 XP |
| Complete any quiz | +20 XP |
| Score ≥ 60% | +15 XP |
| Score ≥ 80% | +30 XP |
| Perfect score (100%) | +50 XP |

### 7 Levels

```
🌱 Seedling (0)  ──►  📖 Reader (50)  ──►  🎓 Student (150)  ──►  🔬 Scholar (300)
──►  🏆 Expert (500)  ──►  🌟 Master (800)  ──►  🚀 Genius (1200)
```

### 15 Badges to Unlock

| Badge | Condition |
|---|---|
| 🎯 First Quiz | Complete your first quiz |
| 💯 Perfect Score | Score 100% on any quiz |
| 🔥 3-Day Streak | Study 3 days in a row |
| ⚡ Week Warrior | Study 7 days in a row |
| 🗓️ Fortnight Hero | Study 14 days in a row |
| 🗺️ Explorer | Study 5 different topics |
| 🧠 Polymath | Study 10 different topics |
| 🧩 Quiz Master | Complete 10 quizzes |
| 🏅 Quiz Champion | Complete 25 quizzes |
| 🎉 High Achiever | Score above 80% |
| 🃏 Card Shark | Complete a flashcard deck |
| 🔬 Scholar | Reach Scholar level (300 XP) |
| 🏆 Expert | Reach Expert level (500 XP) |
| 🌟 Master | Reach Master level (800 XP) |
| 📝 Note Taker | Save your first note |

---

## 💡 Supported Topics

LearnCraft works with **any topic you type**. Built-in suggestions include:

> `Photosynthesis` · `Machine Learning` · `World War II` · `Python Functions` · `Calculus` · `Climate Change` · `The French Revolution` · `DNA Replication` · `Object-Oriented Programming` · `The Solar System` · `Economics Supply & Demand` · `Quantum Mechanics`

---

## 🏗️ Architecture

```
User (Browser)
      │
      ▼
  app.py  (Streamlit — routing, session state, UI)
      │
      ├── content_generator.py  ──┐
      ├── quiz_generator.py       ├──► Groq API (LLaMA-3.3-70b)
      ├── flashcard_generator.py  │
      └── tutor.py             ───┘
      │
      ├── evaluation.py        ── Quiz scoring
      ├── gamification.py      ── XP / badges / streaks
      ├── pdf_export.py        ── ReportLab PDF generation
      └── utils.py             ── JSON file persistence
```

---

## 🔒 Privacy & Data

- All progress, notes and gamification data are stored in **local JSON files**
- No user data is sent anywhere except to the **Groq API** for content generation
- Groq API is used solely for generating educational content
- On Hugging Face Spaces, storage resets when the Space restarts — data is session-loca

<div align="center">

Built with ❤️ using **Streamlit** · **Groq** · **ReportLab** · **Python**

<br>

*🎓 LearnCraft — Learn smarter, not harder.*

</div>
