"""Kids Guess - Game Engine"""

from dataclasses import dataclass, field
from enum import Enum
import random


class GameMode(str, Enum):
    LETTERS = "letters"
    ANIMALS = "animals"
    WORDS = "words"
    MIXED = "mixed"


class Difficulty(str, Enum):
    EASY = "easy"      # ages 3-4
    MEDIUM = "medium"  # ages 5-6
    HARD = "hard"      # ages 7+


@dataclass
class Round:
    number: int
    prompt: str              # What to show on screen
    prompt_type: str         # "letter", "image", "word"
    correct_answer: str      # The expected answer
    accepted_answers: list[str] = field(default_factory=list)  # Synonyms/alternatives
    hint: str = ""
    image_url: str = ""


@dataclass
class GameState:
    player_name: str
    player_age: int
    mode: GameMode
    difficulty: Difficulty
    rounds: list[Round] = field(default_factory=list)
    current_round: int = 0
    score: int = 0
    streak: int = 0
    best_streak: int = 0
    max_rounds: int = 10
    is_active: bool = True

    @property
    def current(self) -> Round | None:
        if 0 <= self.current_round < len(self.rounds):
            return self.rounds[self.current_round]
        return None

    @property
    def is_complete(self) -> bool:
        return self.current_round >= self.max_rounds


def difficulty_from_age(age: int) -> Difficulty:
    if age <= 4:
        return Difficulty.EASY
    elif age <= 6:
        return Difficulty.MEDIUM
    return Difficulty.HARD


# --- Content Banks ---

LETTERS_EASY = [
    Round(0, "A", "letter", "A", ["a", "ay", "eh"], hint="This is the first letter of the alphabet!"),
    Round(0, "B", "letter", "B", ["b", "bee"], hint="This letter sounds like a buzzing insect!"),
    Round(0, "C", "letter", "C", ["c", "see", "sea"], hint="Cat starts with this letter!"),
    Round(0, "D", "letter", "D", ["d", "dee"], hint="Dog starts with this letter!"),
    Round(0, "E", "letter", "E", ["e", "ee"], hint="Elephant starts with this letter!"),
    Round(0, "F", "letter", "F", ["f", "ef"], hint="Fish starts with this letter!"),
    Round(0, "G", "letter", "G", ["g", "gee", "jee"], hint="Giraffe starts with this letter!"),
    Round(0, "H", "letter", "H", ["h", "aitch"], hint="Horse starts with this letter!"),
    Round(0, "I", "letter", "I", ["i", "eye"], hint="Ice cream starts with this letter!"),
    Round(0, "J", "letter", "J", ["j", "jay"], hint="Juice starts with this letter!"),
    Round(0, "K", "letter", "K", ["k", "kay"], hint="Kite starts with this letter!"),
    Round(0, "L", "letter", "L", ["l", "el"], hint="Lion starts with this letter!"),
    Round(0, "M", "letter", "M", ["m", "em"], hint="Monkey starts with this letter!"),
    Round(0, "O", "letter", "O", ["o", "oh"], hint="Orange starts with this letter!"),
    Round(0, "S", "letter", "S", ["s", "es"], hint="Snake starts with this letter!"),
    Round(0, "T", "letter", "T", ["t", "tee"], hint="Tiger starts with this letter!"),
    Round(0, "Z", "letter", "Z", ["z", "zee", "zed"], hint="Zebra starts with this letter!"),
]

ANIMALS_EASY = [
    Round(0, "dog", "image", "dog", ["doggy", "puppy", "pup"], hint="It barks and wags its tail!", image_url="animals/dog.png"),
    Round(0, "cat", "image", "cat", ["kitty", "kitten"], hint="It says meow!", image_url="animals/cat.png"),
    Round(0, "cow", "image", "cow", ["moo", "moo cow"], hint="It says moo and gives us milk!", image_url="animals/cow.png"),
    Round(0, "pig", "image", "pig", ["piggy", "piglet"], hint="It's pink and says oink!", image_url="animals/pig.png"),
    Round(0, "duck", "image", "duck", ["ducky", "duckling"], hint="It says quack!", image_url="animals/duck.png"),
    Round(0, "fish", "image", "fish", ["fishy", "goldfish"], hint="It swims in water!", image_url="animals/fish.png"),
    Round(0, "bird", "image", "bird", ["birdy", "birdie"], hint="It has wings and can fly!", image_url="animals/bird.png"),
    Round(0, "lion", "image", "lion", ["simba"], hint="It's the king of the jungle!", image_url="animals/lion.png"),
    Round(0, "bear", "image", "bear", ["teddy", "teddy bear"], hint="It's big and furry!", image_url="animals/bear.png"),
    Round(0, "frog", "image", "frog", ["froggy", "toad"], hint="It says ribbit and jumps!", image_url="animals/frog.png"),
]

ANIMALS_MEDIUM = ANIMALS_EASY + [
    Round(0, "elephant", "image", "elephant", ["ellie"], hint="It has a long trunk!", image_url="animals/elephant.png"),
    Round(0, "giraffe", "image", "giraffe", [], hint="It has a very long neck!", image_url="animals/giraffe.png"),
    Round(0, "penguin", "image", "penguin", [], hint="It's black and white and lives in the cold!", image_url="animals/penguin.png"),
    Round(0, "monkey", "image", "monkey", ["chimp"], hint="It swings from trees and eats bananas!", image_url="animals/monkey.png"),
    Round(0, "zebra", "image", "zebra", [], hint="It has black and white stripes!", image_url="animals/zebra.png"),
    Round(0, "dolphin", "image", "dolphin", [], hint="It's smart and swims in the ocean!", image_url="animals/dolphin.png"),
]


def _get_content_bank(mode: GameMode, difficulty: Difficulty) -> list[Round]:
    if mode == GameMode.LETTERS:
        return LETTERS_EASY[:]
    elif mode == GameMode.ANIMALS:
        if difficulty == Difficulty.EASY:
            return ANIMALS_EASY[:]
        return ANIMALS_MEDIUM[:]
    elif mode == GameMode.MIXED:
        bank = LETTERS_EASY[:] + ANIMALS_EASY[:]
        return bank
    return LETTERS_EASY[:]


def create_game(
    player_name: str,
    player_age: int,
    mode: GameMode = GameMode.LETTERS,
    max_rounds: int = 10,
) -> GameState:
    """Create a new game session."""
    difficulty = difficulty_from_age(player_age)
    bank = _get_content_bank(mode, difficulty)
    random.shuffle(bank)

    rounds = []
    for i, template in enumerate(bank[:max_rounds]):
        rounds.append(Round(
            number=i + 1,
            prompt=template.prompt,
            prompt_type=template.prompt_type,
            correct_answer=template.correct_answer,
            accepted_answers=template.accepted_answers,
            hint=template.hint,
            image_url=template.image_url,
        ))

    return GameState(
        player_name=player_name,
        player_age=player_age,
        mode=mode,
        difficulty=difficulty,
        rounds=rounds,
        max_rounds=min(max_rounds, len(rounds)),
    )


def check_answer(game: GameState, spoken: str) -> dict:
    """Validate a spoken answer against the current round.

    Returns dict with:
        correct: bool
        score: int (updated)
        streak: int (updated)
        feedback: str ("correct", "close", "wrong")
        move_on: bool (advance to next round)
    """
    if not game.current:
        return {"correct": False, "feedback": "game_over", "move_on": False, "score": game.score, "streak": game.streak}

    answer = spoken.strip().lower()
    target = game.current.correct_answer.lower()
    accepted = [a.lower() for a in game.current.accepted_answers]

    if answer == target or answer in accepted:
        game.score += 1
        game.streak += 1
        game.best_streak = max(game.best_streak, game.streak)
        return {"correct": True, "feedback": "correct", "move_on": True, "score": game.score, "streak": game.streak}

    # Partial match / close
    if target in answer or answer in target:
        game.score += 1
        game.streak += 1
        game.best_streak = max(game.best_streak, game.streak)
        return {"correct": True, "feedback": "close", "move_on": True, "score": game.score, "streak": game.streak}

    game.streak = 0
    return {"correct": False, "feedback": "wrong", "move_on": False, "score": game.score, "streak": game.streak}


def advance_round(game: GameState) -> dict:
    """Move to the next round. Returns round info or game_over."""
    game.current_round += 1
    if game.is_complete:
        game.is_active = False
        return {
            "status": "game_over",
            "final_score": game.score,
            "max_rounds": game.max_rounds,
            "best_streak": game.best_streak,
        }

    r = game.current
    return {
        "status": "next_round",
        "round": r.number,
        "prompt": r.prompt,
        "prompt_type": r.prompt_type,
        "image_url": r.image_url,
        "score": game.score,
        "streak": game.streak,
    }
