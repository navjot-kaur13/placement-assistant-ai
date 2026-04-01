def persona_engine(resume_text, persona):
    persona_feedback = {
        "Recruiter": (
            "📌 **Recruiter's View:** Your resume is clear, but I'm looking for 'Impact'. "
            "Use numbers like 'Increased efficiency by 20%'. "
            "Make sure your contact info is easy to find."
        ),
        "Hiring Manager": (
            "🛠️ **Hiring Manager's View:** Your technical skills are good, but I need to see "
            "the 'Depth' of your projects. Mention specific challenges and how you solved them."
        ),
        "CTO": (
            "🚀 **CTO's View:** I'm looking for architectural understanding. "
            "Explain *why* you chose a particular tech stack. Show me you understand scalability."
        )
    }

    return persona_feedback.get(
        persona, 
        "🔍 **General Feedback:** Your resume is a great start! Focus on tailoring it to the specific job role."
    )