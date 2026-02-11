import re


def analyze_skill_depth(resume_text, skills):
    resume_text = resume_text.lower()

    depth_result = {}

    for skill in skills:
        pattern = rf"{skill}(.{{0,50}})"
        matches = re.findall(pattern, resume_text)

        score = 0
        for match in matches:
            if any(word in match for word in ["expert", "advanced", "lead", "5+", "senior"]):
                score += 3
            elif any(word in match for word in ["intermediate", "experienced", "3+"]):
                score += 2
            elif any(word in match for word in ["basic", "familiar", "beginner", "1+"]):
                score += 1

        if score >= 3:
            depth = "Expert"
        elif score == 2:
            depth = "Intermediate"
        elif score == 1:
            depth = "Beginner"
        else:
            depth = "Mentioned"

        depth_result[skill] = depth

    return depth_result
