def detect_risks(resume_text):
    risks = []

    if "lorem ipsum" in resume_text.lower():
        risks.append("Placeholder text detected")

    if resume_text.lower().count("responsible for") > 3:
        risks.append("Too many weak bullet phrases ('Responsible for')")

    if len(resume_text.split()) < 150:
        risks.append("Resume content too short")

    if len(resume_text.split()) > 1200:
        risks.append("Resume content too long")

    if not any(char.isdigit() for char in resume_text):
        risks.append("No measurable metrics found (numbers missing)")

    return risks
