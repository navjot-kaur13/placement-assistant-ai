import re

def ats_engine(resume_text):
    score = 0

    # -----------------------------
    # 1. Keywords
    # -----------------------------
    keywords = [
        "python", "java", "sql", "machine learning",
        "data analysis", "react", "node", "project",
        "internship", "developer", "api"
    ]

    keyword_matches = sum(1 for word in keywords if word in resume_text.lower())
    keyword_score = min(keyword_matches * 5, 30)
    score += keyword_score

    # -----------------------------
    # 2. Sections
    # -----------------------------
    sections = ["education", "skills", "projects", "experience"]

    section_matches = sum(1 for sec in sections if sec in resume_text.lower())
    section_score = section_matches * 5
    score += section_score

    # -----------------------------
    # 3. Action Verbs
    # -----------------------------
    action_verbs = [
        "developed", "built", "created", "designed",
        "implemented", "analyzed", "improved"
    ]

    verb_matches = sum(1 for verb in action_verbs if verb in resume_text.lower())
    verb_score = min(verb_matches * 3, 15)
    score += verb_score

    # -----------------------------
    # 4. Impact (Numbers)
    # -----------------------------
    numbers = re.findall(r"\d+", resume_text)

    if len(numbers) >= 5:
        impact_score = 15
    elif len(numbers) >= 2:
        impact_score = 10
    else:
        impact_score = 5

    score += impact_score

    # -----------------------------
    # FINAL OUTPUT (DICT)
    # -----------------------------
    return {
        "total": min(score, 100),
        "keywords": keyword_score,
        "sections": section_score,
        "verbs": verb_score,
        "impact": impact_score
    }