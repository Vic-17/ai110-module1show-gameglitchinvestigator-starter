def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard was returning 1-50 (easier than Normal). Corrected to 1-200.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200  # FIXED: was 1-50, which is easier than Normal. Hard should be wider.
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py using Copilot Agent mode.
    if raw is None:
        return False, None, "Enter a guess."
    if raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome: "Win", "Too High", or "Too Low"
    """
    # FIX: Messages were inverted. "Go HIGHER!" appeared when guess was too high.
    # Also removed the string-comparison fallback — secret should always be an int.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"   # FIXED: was "Go HIGHER!" — completely backwards
    return "Too Low", "📈 Go HIGHER!"        # FIXED: was "Go LOWER!" — completely backwards


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Original code rewarded wrong guesses (+5 for "Too High" on even attempts).
    # Now only a win gains points; wrong guesses always cost points.
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points
    if outcome in ("Too High", "Too Low"):
        return current_score - 5   # FIXED: was giving +5 on even attempts for wrong guesses
    return current_score
