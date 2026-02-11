def persona_engine(resume_text, persona):
    persona_feedback = {
        "Recruiter": "Your resume is clear but could use stronger impact metrics.",
        "Hiring Manager": "Your technical skills are relevant, but project depth can be improved.",
        "ATS Bot": "Your resume is ATS-friendly but needs more keyword optimization."
    }

    return persona_feedback.get(
        persona,
        "Your resume looks good but can be improved with more clarity."
    )

