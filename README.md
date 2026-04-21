# 🟩 Wordle App — Full Stack

A full stack Wordle clone built with a Python Flask backend and vanilla JavaScript frontend. Guess the 5-letter word in 6 tries!

🎮 **[Play it live here](https://anaghamalladi.github.io/wordle-app)**

---

## Features
- 🎯 Real-time word validation against a dictionary
- 🟩 Color-coded feedback — green, yellow, and gray tiles
- ⌨️ Physical keyboard + on-screen keyboard support
- 🔄 Flip animations on guess submission
- 📳 Shake animation on invalid words
- 📊 Stats tracker — wins, streak, and guess distribution
- 🔁 New Game button to restart without refreshing

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-CORS |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Deployment | Render (backend), GitHub Pages (frontend) |

---

## How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
Open `frontend/index.html` with Live Server in VS Code.

---
## Project Structure
wordle-app/
├── backend/
│   ├── app.py
│   └── requirements.txt
└── docs/
├── index.html
├── style.css
└── game.js

---

Built by [Anagha Malladi](https://github.com/anaghamalladi)
