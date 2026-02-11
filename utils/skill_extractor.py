import spacy
import pandas as pd
from pathlib import Path

nlp = spacy.load("en_core_web_sm")


def load_skill_database():
    skill_file = Path("data/skills.csv")
    if not skill_file.exists():
        return set()

    df = pd.read_csv(skill_file)
    return set(df["skill"].str.lower())


def extract_skills(resume_text):
    skills_db = load_skill_database()
    found_skills = set()

    doc = nlp(resume_text.lower())

    for token in doc:
        if token.text in skills_db:
            found_skills.add(token.text)

    for chunk in doc.noun_chunks:
        if chunk.text.strip() in skills_db:
            found_skills.add(chunk.text.strip())

    return sorted(found_skills)
