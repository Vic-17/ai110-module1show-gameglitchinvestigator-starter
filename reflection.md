# Game Glitch Investigator – Reflection

---

## 1. What was broken when you started?

**Bug 1 – Inverted hints (Too High / Too Low)**
- **Expected:** When I guessed a number higher than the secret, the game should tell me to go lower.
- **What happened:** The game said "Go HIGHER!" even when my guess was already too high. The messages were completely backwards — "Too High" showed "📈 Go HIGHER!" and "Too Low" showed "📉 Go LOWER!", which is the opposite of what they should say.

**Bug 2 – String/integer type mixing**
- **Expected:** The secret number should always be compared numerically to my guess.
- **What happened:** On every even-numbered attempt, `app.py` converted the secret to a string using `str(st.session_state.secret)`. This meant the comparison `check_guess(60, "50")` triggered a string comparison (`"60" > "50"` is True alphabetically but can produce unexpected results), making the outcome unreliable. You could guess the exact right number and still not win on an even attempt if the string logic misfired.

**Bug 3 – Hard difficulty was actually easier than Normal**
- **Expected:** Hard mode should have a wider range of possible numbers, making it harder to guess.
- **What happened:** `get_range_for_difficulty("Hard")` returned `1–50`, which is a *smaller* range than Normal's `1–100`. Selecting "Hard" made the game easier, not harder.

**Bonus Bug 4 – Score rewarded wrong guesses**
- **Expected:** Getting the wrong answer should never increase your score.
- **What happened:** `update_score` gave +5 points for a "Too High" outcome on even-numbered attempts. You could farm points by guessing wrong repeatedly.

---

## 2. How did you use AI as a teammate?

**Correct AI suggestion:**
I used Copilot to help identify the inverted-hints bug. When I highlighted the `check_guess` function and asked "Explain this logic step by step," it correctly pointed out that the return labels didn't match the messages — "Too High" was paired with "Go HIGHER!" which contradicts itself. Copilot's explanation was accurate and I verified it by playing the game: guessing 80 when the secret was 30 told me to go higher, which confirmed the hints were backwards. The fix — swapping the two messages — worked immediately.

**Incorrect / misleading AI suggestion:**
When I asked Copilot to explain the `update_score` function, it initially described the +5 points on even attempts as an intentional "streak bonus" feature rather than a bug. This was misleading — the design makes no sense because you're rewarded for guessing wrong. I rejected this interpretation because the project description says the game is intentionally broken, and giving points for wrong guesses is clearly a glitch. I verified by running the game and watching the score increase after a wrong "Too High" guess on attempt 2.

---

## 3. Debugging and testing your fixes

**Fix 1 – Inverted hints:**
I swapped the messages in `check_guess` inside `logic_utils.py`:
- `"Too High"` now returns `"📉 Go LOWER!"`
- `"Too Low"` now returns `"📈 Go HIGHER!"`

Verified by: running the game and guessing 80 with secret 30 — correctly showed "Go LOWER!". Also confirmed by `test_check_guess_too_high` and `test_check_guess_too_low` in pytest.

**Fix 2 – String/int type mixing:**
In `app.py`, I removed the conditional that converted the secret to a string on even attempts:
```python
# BEFORE (buggy):
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
else:
    secret = st.session_state.secret

# AFTER (fixed):
secret = st.session_state.secret
```
I also removed the string-comparison fallback in `check_guess` since it's no longer needed. Verified by guessing the exact secret number on both odd and even attempts — now correctly shows "Win" every time.

**Fix 3 – Hard difficulty range:**
Changed `get_range_for_difficulty("Hard")` from returning `1, 50` to `1, 200`. Verified by `test_hard_range_is_wider_than_normal` in pytest, and by checking the sidebar in the Streamlit app showing "Range: 1 to 200" when Hard is selected.

---

## 4. Final Reflection

**What did you learn about reading AI-generated code?**
AI-generated code can look clean and professional while containing bugs that are easy to miss on a quick scan. The type-mixing bug in particular — converting the secret to a string on even attempts — was buried inside an `if/else` that looked almost intentional. I learned to read logic slowly and ask "why would this condition ever need to exist?" as a red flag for suspicious code.

**When should you accept vs. reject AI suggestions?**
I should accept AI suggestions when they match observable behavior in the game and make logical sense. I rejected the "streak bonus" explanation for the score bug because it didn't align with what a guessing game should do — wrong guesses shouldn't be rewarded. The rule I'd use: if an AI explanation requires you to invent a justification for clearly broken behavior, reject it and trust your own reasoning.

**How did human judgment matter here?**
At every step, I had to decide whether the AI's explanation or suggestion actually matched reality. Copilot was useful for spotting surface-level inconsistencies like the swapped messages, but it couldn't tell me whether the score behavior was a feature or a bug — that required me to think about what the game is *supposed* to do. Human judgment was the deciding factor in every fix.
