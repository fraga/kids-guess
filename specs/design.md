# Kids Guessing Game Web App (Realtime Voice Agent)

A kid-friendly web game where a realtime voice agent hosts a guessing game.

The agent shows letters, words, or pictures on the screen and asks the child to guess by speaking the answer. The app validates the answer, keeps score, and adapts the experience based on the player's name and age.

## Core Idea

Use AI for interaction, not for core game logic.

- AI handles voice conversation, encouragement, hints, and pacing.
- Your backend/game engine remains the source of truth for:
  - current round
  - correct answer
  - accepted answers/synonyms
  - score
  - streaks
  - timers
  - difficulty progression

This makes the game reliable and easier to debug.

## Goals

- Kid-friendly "playground" feel
- Voice-based gameplay (child answers by speaking)
- Age-adaptive prompts and difficulty
- Real-time validation and scoring
- Safe, curated experience for children

## High-Level Architecture

### 1) Frontend (Playground Webpage)
Recommended: React / Next.js

Responsibilities:
- Full-screen kid-friendly UI
- Canvas/screen area to present:
  - letters
  - words
  - pictures
  - simple animations
- Big controls:
  - Start
  - Repeat clue
  - Skip
  - Mute
- Player setup:
  - Name
  - Age
  - Mode (letters / words / animals / mixed)

### 2) Realtime Voice Layer
Two implementation options:

#### Option A: Simpler MVP
- Browser captures microphone audio
- Frontend sends audio to backend
- Backend calls AI (Realtime API or Responses API flow)
- Backend returns:
  - agent speech/audio
  - structured action (hint / retry / praise / next round)

Pros:
- easier to build first
- easier to control/debug

#### Option B: Better UX / Lower Latency
- WebRTC-style realtime audio streaming
- Agent can speak naturally and be interrupted
- Frontend receives live agent events + audio

Pros:
- smoother user experience
- more natural turn-taking

### 3) Backend Game Engine (Authoritative)
This is the most important piece.

Responsibilities:
- Generate rounds
- Select difficulty based on age
- Store current target answer
- Validate child answer
- Keep score/streaks
- Manage session state
- Decide round transitions

The backend should own:
- `currentAnswer`
- `acceptedAnswers[]`
- `score`
- `streak`
- `roundNumber`
- `maxRounds`
- `timeRemaining` (if timed)

## Stack Options

| Layer | Option A (MVP) | Option B (Production) |
|-------|---------------|----------------------|
| Frontend | React / Next.js | React / Next.js |
| Voice capture | MediaRecorder API | WebRTC |
| AI voice | OpenAI Responses API | OpenAI Realtime API |
| Backend | FastAPI or Next.js API routes | FastAPI + WebSocket |
| Game state | In-memory / Redis | Redis / DB |
| TTS | OpenAI TTS or ElevenLabs | OpenAI Realtime (native) |
| STT | OpenAI Whisper | OpenAI Realtime (native) |

## Game Modes

- **Letters** (age 3-5): Show a letter, child says the letter or a word starting with it
- **Words** (age 4-6): Show a picture, child says the word
- **Animals** (age 3-7): Animal sounds or images, child names the animal
- **Mixed** (age 5+): Combination of all modes

## Content Safety

- All content pre-curated (no AI-generated images/words in gameplay)
- Voice agent system prompt enforces kid-friendly language
- No user data stored beyond session
- Parental gate for settings/configuration

## MVP Scope

1. Single game mode (letters or animals)
2. Option A voice flow (simpler)
3. 10 rounds per game
4. Basic scoring (correct/incorrect)
5. Age selection (3-5, 5-7)
6. One AI voice personality
7. Desktop browser only (mobile later)
