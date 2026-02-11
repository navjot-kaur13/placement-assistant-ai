import re
import pandas as pd
from pathlib import Path


def load_action_verbs():
    verb_file = Path("data/action_verbs.csv")
    if not verb_file.exists():
        return set()

    df = pd.read_csv(verb_file)
    return set(df["verb"].str.lower())


def analyze_bullets(resume_text):
    action_verbs = load_action_verbs()
    bullets = re.split(r"[\n•\-]", resume_text)

    analysis = []

    for bullet in bullets:
        bullet = bullet.strip()
        if len(bullet) < 20:
            continue

        words = bullet.lower().split()
        starts_with_action = words[0] in action_verbs if words else False
        has_metrics = bool(re.search(r"\d+%", bullet)) or bool(re.search(r"\d+\s*(users|projects|clients)", bullet.lower()))

        score = 0
        if starts_with_action:
            score += 1
        if has_metrics:
            score += 1

        analysis.append({
            "bullet": bullet,
            "starts_with_action": starts_with_action,
            "has_metrics": has_metrics,
            "quality": "Strong" if score == 2 else "Weak"
        })

    return analysis
