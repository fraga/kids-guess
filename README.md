# Kids Guess

Kid-friendly voice guessing game powered by AI.

A realtime voice agent hosts a guessing game -- showing letters, words, or pictures on screen while a child answers by speaking. The AI handles conversation and encouragement; the backend owns all game logic.

## Stack

- **Frontend:** Next.js (React)
- **Backend:** FastAPI (Python)
- **Voice:** OpenAI Realtime API / Whisper + TTS
- **Game Engine:** Python (authoritative server-side logic)

## Project Structure

```
kids-guess/
  frontend/          # Next.js app
  backend/           # FastAPI server + game engine
  content/           # Curated game content (letters, words, images)
  specs/             # Design docs
```

## Getting Started

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## License

MIT
