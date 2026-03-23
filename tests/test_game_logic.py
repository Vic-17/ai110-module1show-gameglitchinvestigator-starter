import pytest
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# --- check_guess tests ---

def test_check_guess_correct():
    outcome, message = check_guess(42, 42)
    assert outcome == "Win"

def test_check_guess_too_high():
    # Guess of 60 against secret of 50 — should say Too High, not Too Low
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message  # FIX verified: hint now correctly says go lower

def test_check_guess_too_low():
    # Guess of 30 against secret of 50 — should say Too Low
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message  # FIX verified: hint now correctly says go higher

def test_check_guess_types_are_ints():
    # Secret should always be compared as int, never as string (was a bug in app.py)
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# --- parse_guess tests ---

def test_parse_guess_valid():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err is not None

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False

def test_parse_guess_decimal_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7


# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_range_is_wider_than_normal():
    # FIX verified: Hard was 1-50 (easier than Normal). Now Hard must be wider.
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high


# --- update_score tests ---

def test_win_increases_score():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_wrong_guess_decreases_score():
    # FIX verified: original code gave +5 for "Too High" on even attempts
    score_after_too_high = update_score(50, "Too High", 2)
    assert score_after_too_high < 50

def test_too_low_decreases_score():
    score_after_too_low = update_score(50, "Too Low", 1)
    assert score_after_too_low < 50
