import re

def ats_engine(resume_text):
    score = 0
    text_lower = resume_text.lower()

    # -----------------------------
    # 1. Keywords (Expanded List for Variation)
    # -----------------------------
    keywords = [
        "python", "java", "sql", "machine learning", "data analysis", "react", 
        "node", "api", "cloud", "aws", "docker", "kubernetes", "git", "github",
        "rest", "backend", "frontend", "full stack", "mongodb", "postgresql",
        "unit testing", "agile", "scrum", "devops", "cicd", "typescript", "tableau"
    ]

    keyword_matches = sum(1 for word in keywords if word in text_lower)
    # Scoring variation: Ab 15+ keywords chahiye 30 points ke liye
    keyword_score = min(keyword_matches * 2, 30) 
    score += keyword_score

    # -----------------------------
    # 2. Sections (Checking for standard headers)
    # -----------------------------
    sections = [
        "education", "skills", "projects", "experience", 
        "certifications", "languages", "summary", "objective"
    ]

    section_matches = sum(1 for sec in sections if sec in text_lower)
    # Ab har section ke 3 points, max 20
    section_score = min(section_matches * 3, 20) 
    score += section_score

    # -----------------------------
    # 3. Action Verbs (Strict Checking)
    # -----------------------------
    action_verbs = [
        "developed", "built", "created", "designed", "implemented", 
        "analyzed", "improved", "led", "managed", "optimized", 
        "coordinated", "collaborated", "reduced", "increased", "solved"
    ]

    verb_matches = sum(1 for verb in action_verbs if verb in text_lower)
    # 1 point per unique verb, max 15
    verb_score = min(verb_matches * 1.5, 15) 
    score += verb_score

    # -----------------------------
    # 4. Impact (Real Data Analysis)
    # -----------------------------
    # Hum sirf numbers nahi, percentage ya currency bhi dhundenge
    impact_patterns = [r"\d+%", r"\$\d+", r"\d+ \+", r"percent"]
    has_impact = any(re.search(p, text_lower) for p in impact_patterns)
    
    numbers = re.findall(r"\d+", resume_text)

    if has_impact and len(numbers) >= 5:
        impact_score = 15
    elif len(numbers) >= 3:
        impact_score = 10
    else:
        impact_score = 5

    score += impact_score

    # -----------------------------
    # 5. Length Penalty/Bonus (New Dynamic Logic)
    # -----------------------------
    word_count = len(resume_text.split())
    if 200 <= word_count <= 600:
        score += 20  # Perfect length
    else:
        score += 10  # Too short or too long

    # FINAL OUTPUT
    return {
        "total": int(min(score, 100)),
        "keywords": int(keyword_score),
        "sections": int(section_score),
        "verbs": int(verb_score),
        "impact": int(impact_score)
    }