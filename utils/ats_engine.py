def ats_engine(resume_text):
    """
    Simple ATS scoring logic
    """

    score = 0

    keywords = [
        "python", "java", "sql", "machine learning",
        "data analysis", "project", "experience",
        "internship", "api", "cloud"
    ]

    resume_text = resume_text.lower()

    for word in keywords:
        if word in resume_text:
            score += 10

    if score > 100:
        score = 100

    return score

