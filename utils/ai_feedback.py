def generate_ai_feedback(
    skills,
    skill_depths,
    ats_result,
    jd_result,
    bullet_analysis,
    risk_flags,
    simulations,
    personas
):
    feedback = {}

    feedback["Overall Summary"] = (
        f"Your resume shows proficiency in {len(skills)} key skills. "
        f"ATS score is {ats_result['ats_score']} and JD match is {jd_result['match_percentage']}%."
    )

    feedback["Skills"] = {
        "detected_skills": skills,
        "skill_depths": skill_depths
    }

    feedback["ATS Feedback"] = ats_result["ats_feedback"]

    feedback["Bullet Point Review"] = bullet_analysis

    feedback["Risk Flags"] = risk_flags

    feedback["Improvement Simulation"] = simulations

    feedback["Persona Views"] = personas

    return feedback
