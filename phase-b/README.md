# Phase B — the full-stack version (work in progress)

This folder is the **v2 rebuild** of Decode Your Pattern as a real full-stack app.
It does **not** affect your live v1 (which is still the HTML files in the repo root).

We're building it in small, safe sub-steps:

| Sub-step | What | Status |
|---|---|---|
| **B1** | **Backend** — FastAPI + the scoring engine + AI Coach | ✅ done (this folder's `backend/`) |
| B2 | Frontend — React + TypeScript + Tailwind | ⏳ next |
| B3 | Database + saved reports | ⏳ |
| B4 | Login (Google/GitHub) + guest mode | ⏳ |
| B5 | Analytics dashboard + deploy | ⏳ |

---

# 🟢 Getting started with the backend (beginner-friendly, Windows)

You'll install Python once, then run the server with a couple of commands. Take it slow — every line below is copy-paste.

## 1. Install the tools (one time)

1. **Python** — go to <https://www.python.org/downloads/> → click the big **Download Python** button.
   - **IMPORTANT:** on the first install screen, tick the box **"Add Python to PATH"**, then click Install.
2. **VS Code** (a friendly code editor, optional but recommended) — <https://code.visualstudio.com/>.

To check Python installed: open the **Start menu**, type `cmd`, open **Command Prompt**, and run:
```cmd
python --version
```
You should see something like `Python 3.12.x`. (If it says "not recognised", restart your PC and try again.)

## 2. Open a terminal in the backend folder

In **Command Prompt**, paste this (it moves into the backend folder):
```cmd
cd "D:\OneDrive\Desktop\AI Road Map\Decode_Your_Pattern\phase-b\backend"
```

## 3. Create a "virtual environment" (a clean sandbox for this project)
```cmd
python -m venv .venv
.venv\Scripts\activate
```
After this your prompt shows `(.venv)` at the start — that means it worked.

## 4. Install the project's libraries
```cmd
pip install -r requirements.txt
```
This downloads FastAPI and friends (takes a minute).

## 5. Run the server 🎉
```cmd
uvicorn app.main:app --reload
```
You'll see `Uvicorn running on http://127.0.0.1:8000`.

## 6. Try it in your browser
Open **<http://127.0.0.1:8000/docs>**

This is an **interactive API page** (auto-generated). You can:
- Open **GET `/api/v1/quiz/questions`** → **Try it out** → **Execute** → see real questions come back.
- Open **POST `/api/v1/assessments`** → **Try it out**, paste a few responses (copy from the questions you got), **Execute** → see a full report with a Pattern Score, insights, avatar, recommendations.
- Open **POST `/api/v1/coach/message`** → send `{"message":"I'm nervous about a job change","report":{...}}` → get a coach reply.

To stop the server, press **Ctrl + C** in the terminal.

## 7. Run the tests (optional, proves it works)
```cmd
pytest
```
You should see all tests pass (green dots).

---

## 🤖 Turning on the real AI Coach (optional, free)

By default the coach gives a smart **rule-based** reply — no key needed. To make it a **real AI**:

1. Get a **free** API key from <https://console.groq.com> (sign up, create an API key).
2. In the `backend` folder, copy `.env.example` to a new file named `.env`.
3. Open `.env` and paste your key after `LLM_API_KEY=`.
4. Restart the server (Ctrl+C, then `uvicorn app.main:app --reload`).

The coach will now answer using a real language model. Your key stays **only** in `.env`
on your computer (it's git-ignored — never uploaded).

---

## What's inside `backend/`
```
backend/
├── app/
│   ├── main.py          # FastAPI app (start here)
│   ├── engine.py        # the explainable scoring engine (pure functions)
│   ├── data.py          # questions, dimensions, recommendations
│   ├── schemas.py       # request/response shapes (validation)
│   └── routers/
│       ├── assessments.py  # /quiz/questions, /assessments
│       └── coach.py        # /coach/message (AI Coach)
├── tests/test_engine.py # unit tests
├── requirements.txt     # libraries to install
├── Dockerfile           # for deploying to Render/Fly later
└── .env.example         # copy to .env for your AI key
```

When you've got the server running and `/docs` open, you've successfully run a real backend. 🎉
Tell the assistant **"backend running"** and we'll build the **React frontend (B2)** next.
