def simulate_improvements(ats_score, jd_match):
    simulations = []

    if ats_score < 70:
        simulations.append(
            "Adding clearer section headings and reducing symbols could increase ATS score by ~10–15 points."
        )

    if jd_match < 60:
        simulations.append(
            "Including missing job description keywords could improve JD match by ~20%."
        )

    if ats_score >= 85 and jd_match >= 70:
        simulations.append(
            "Resume is already strong; focus on tailoring for specific companies."
        )

    return simulations
