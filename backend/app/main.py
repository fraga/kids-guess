"""Kids Guess - FastAPI server."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid

from app.engine import create_game, check_answer, advance_round, GameState, GameMode

load_dotenv()

app = FastAPI(title="Kids Guess", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (swap for Redis in production)
sessions: dict[str, GameState] = {}


class NewGameRequest(BaseModel):
    player_name: str
    player_age: int
    mode: str = "letters"
    max_rounds: int = 10


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/game/new")
async def new_game(req: NewGameRequest):
    """Start a new game session."""
    try:
        mode = GameMode(req.mode)
    except ValueError:
        raise HTTPException(400, f"Invalid mode: {req.mode}. Use: letters, animals, words, mixed")

    game = create_game(
        player_name=req.player_name,
        player_age=req.player_age,
        mode=mode,
        max_rounds=req.max_rounds,
    )

    session_id = str(uuid.uuid4())
    sessions[session_id] = game

    first_round = game.current
    return {
        "session_id": session_id,
        "player_name": game.player_name,
        "difficulty": game.difficulty.value,
        "max_rounds": game.max_rounds,
        "round": {
            "number": first_round.number,
            "prompt": first_round.prompt,
            "prompt_type": first_round.prompt_type,
            "image_url": first_round.image_url,
        },
    }


@app.post("/game/answer")
async def submit_answer(req: AnswerRequest):
    """Submit a spoken answer for the current round."""
    game = sessions.get(req.session_id)
    if not game:
        raise HTTPException(404, "Session not found")
    if not game.is_active:
        raise HTTPException(400, "Game is already over")

    result = check_answer(game, req.answer)

    if result["move_on"]:
        next_info = advance_round(game)
        result["next"] = next_info

    return result


@app.post("/game/skip")
async def skip_round(session_id: str):
    """Skip the current round."""
    game = sessions.get(session_id)
    if not game:
        raise HTTPException(404, "Session not found")
    if not game.is_active:
        raise HTTPException(400, "Game is already over")

    game.streak = 0
    next_info = advance_round(game)
    return {"skipped": True, **next_info}


@app.get("/game/hint")
async def get_hint(session_id: str):
    """Get a hint for the current round."""
    game = sessions.get(session_id)
    if not game:
        raise HTTPException(404, "Session not found")
    if not game.current:
        raise HTTPException(400, "No active round")

    return {"hint": game.current.hint}


@app.get("/game/state")
async def get_state(session_id: str):
    """Get current game state."""
    game = sessions.get(session_id)
    if not game:
        raise HTTPException(404, "Session not found")

    current = game.current
    return {
        "player_name": game.player_name,
        "score": game.score,
        "streak": game.streak,
        "best_streak": game.best_streak,
        "current_round": game.current_round + 1,
        "max_rounds": game.max_rounds,
        "is_active": game.is_active,
        "round": {
            "number": current.number,
            "prompt": current.prompt,
            "prompt_type": current.prompt_type,
            "image_url": current.image_url,
        } if current else None,
    }
