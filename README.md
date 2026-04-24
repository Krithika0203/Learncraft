# 🎓 LearnCraft — Personalized AI Learning Platform

> Generate personalized study material, flashcards & quizzes tailored exactly to your level and learning goals — powered by **Groq LLaMA-3.3-70b**.

![Python](https://img.shields.io/badge/Python-3.9+-6C47FF?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA--3.3--70b-F97316?style=flat-square&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10B981?style=flat-square)

---

## 🌟 What is LearnCraft?

LearnCraft is a fully AI-powered learning platform that generates **customized study content** based on your chosen topic and difficulty level. Whether you're a beginner learning Python or an advanced student studying Quantum Mechanics — LearnCraft adapts everything to you.

### How it works:
1. **Pick a topic** — anything from Calculus to Climate Change
2. **Choose your level** — Beginner, Intermediate, or Advanced
3. **Get personalized content** — notes, quizzes, flashcards and an AI tutor instantly
4. **Track your progress** — earn XP, unlock badges and monitor your scores

---

## ✨ Features

| Feature | Description |
|---|---|
| 📚 **Study Content Generator** | AI-generated notes in 4 styles: Summary Notes, Detailed Explanation, Bullet Points, Concept Map |
| 🃏 **Flashcard Studio** | Auto-generated flip-card decks (up to 20 cards) for any topic |
| 🧩 **Quiz Engine** | MCQ, True/False, Fill-in-the-Blank, Short Answer — with optional timed mode |
| 🤖 **AI Tutor Chat** | Multi-turn conversational AI tutor with topic context and full conversation memory |
| 🏅 **Gamification** | XP points, 7 levels (Seedling → Genius), 15 badges, daily streak tracking |
| 📄 **PDF Export** | Download study notes and quiz results as branded A4 PDFs |
| 📊 **Progress Dashboard** | Score history chart, per-topic best scores, weak topic detection |
| 📝 **Notes** | Save, search and delete personal notes during study sessions |

---

## 🚀 Running on Hugging Face Spaces

This app runs directly on Hugging Face Spaces using the **Streamlit SDK**.

### ⚙️ Required Secret

You must add your **Groq API key** as a Space secret for the app to work:

1. Go to your Space → **Settings** → **Repository secrets**
2. Add a new secret:
   - **Name:** `GROQ_API_KEY`
   - **Value:** your Groq API key from [console.groq.com](https://console.groq.com)

> Get a free Groq API key at **https://console.groq.com** — it takes under a minute.

### 📂 Files required in your Space

```
app.py
content_generator.py
quiz_generator.py
flashcard_generator.py
tutor.py
evaluation.py
gamification.py
pdf_export.py
utils.py
requirements.txt
README.md
```

---

## 🔑 API Key Configuration

The app reads the Groq API key from the environment. Make sure each module uses:

```python
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
```

> If you're running **locally**, set the variable in your terminal:
> ```bash
> export GROQ_API_KEY="gsk_your_key_here"   # macOS/Linux
> set GROQ_API_KEY=gsk_your_key_here         # Windows
> ```

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

## 🗺️ App Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Hero banner, feature overview, quick-start buttons, recent activity feed |
| 📚 **Study Content** | Generate AI study notes with key terms, summary and PDF export |
| 🃏 **Flashcards** | Navigate AI-generated flip cards with progress bar and deck overview |
| 🧩 **Take Quiz** | Timed quiz with instant results, XP awards and PDF download |
| 🤖 **AI Tutor** | Chat with an AI tutor — quick-start prompts and topic context |
| 🏅 **Achievements** | XP level hero card, badge gallery, streak and stats |
| 📊 **My Progress** | Score history, per-topic performance table, weak topic alerts |
| 📝 **My Notes** | Searchable saved notes from study sessions |

---

## 🏅 Gamification

### Earn XP for every learning action:

| Action | XP |
|---|---|
| Study session | +10 XP |
| Flashcard deck | +10 XP |
| Complete a quiz | +20 XP |
| Score ≥ 60% | +15 XP |
| Score ≥ 80% | +30 XP |
| Perfect score (100%) | +50 XP |

### 7 Levels:
```
🌱 Seedling (0 XP)  →  📖 Reader (50)  →  🎓 Student (150)  →  🔬 Scholar (300)
→  🏆 Expert (500)  →  🌟 Master (800)  →  🚀 Genius (1200)
```

### 15 Badges to unlock:
| Badge | How to Earn |
|---|---|
| 🎯 First Quiz | Complete your first quiz |
| 💯 Perfect Score | Score 100% on a quiz |
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

## 📐 Architecture

```
User (Browser)
      │
      ▼
app.py  (Streamlit — routing, session state, UI)
      │
      ├── content_generator.py  ──┐
      ├── quiz_generator.py       ├──► Groq API (LLaMA-3.3-70b)
      ├── flashcard_generator.py  │
      ├── tutor.py             ───┘
      │
      ├── evaluation.py        ── Quiz answer scoring
      ├── gamification.py      ── XP / badges / streak
      ├── pdf_export.py        ── ReportLab PDF generation
      └── utils.py             ── JSON persistence
                                   (learning_progress.json,
                                    notes.json,
                                    gamification.json)
```

---

## 💡 Topics You Can Study

LearnCraft works with **any topic you type**, plus these built-in suggestions:

`Photosynthesis` · `Machine Learning` · `World War II` · `Python Functions` · `Calculus` · `Climate Change` · `The French Revolution` · `DNA Replication` · `Object-Oriented Programming` · `The Solar System` · `Economics Supply & Demand` · `Quantum Mechanics`

---

## 🔒 Data & Privacy

- All progress, notes and gamification data are stored in **local JSON files** within the Space
- No user data is sent anywhere except to the **Groq API** for content generation
- The Groq API is used solely for generating educational content
- On Hugging Face Spaces, persistent storage resets when the Space restarts — data is session-local

---

## 🛠️ Local Development

```bash
# 1. Clone the Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/learncraft
cd learncraft

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export GROQ_API_KEY="gsk_your_key_here"

# 4. Run
streamlit run app.py
```

---

## 📄 License

MIT License — free to use, modify and distribute.

---

<div align="center">
  Built with ❤️ using <strong>Streamlit</strong> · <strong>Groq</strong> · <strong>ReportLab</strong> · <strong>Python</strong>
  <br><br>
  <em>🎓 LearnCraft — Learn smarter, not harder.</em>
</div>
