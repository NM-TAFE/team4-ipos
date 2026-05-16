import json
import os

SCORE_FILE = "score.json"


def load_score():
    """Load score from score.json if it exists."""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        except (OSError, json.JSONDecodeError, ValueError):
            pass

    return {"X": 0, "O": 0, "draws": 0}


def save_score(score):
    """Save score to score.json."""
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(score, f, indent=2)
