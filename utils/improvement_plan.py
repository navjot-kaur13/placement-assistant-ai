def generate_plan(ats_score, jd_score, risks):
    plan = []

    # ATS based suggestions
    if ats_score < 60:
        plan.append("Improve your resume structure and add more relevant skills.")
        plan.append("Enhance project descriptions with clear impact.")
    elif ats_score < 80:
        plan.append("Optimize resume with better keywords.")
        plan.append("Add measurable achievements (numbers, results).")
    else:
        plan.append("Your resume is strong. Focus on fine-tuning.")

    # JD match suggestions
    if jd_score < 50:
        plan.append("Customize your resume based on the job description.")
        plan.append("Add missing skills mentioned in the JD.")
    elif jd_score < 75:
        plan.append("Improve alignment with job requirements.")
    else:
        plan.append("Good alignment with job description.")

    # Risk suggestions
    if risks:
        plan.append("Fix highlighted issues in your resume.")

    return plan