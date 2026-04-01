def persona_engine(resume_text, persona):
    # Dictionary of specific feedback for each role
    persona_feedback = {
        "Recruiter": (
            "📌 **Recruiter's View:** Your resume is clear, but I'm looking for 'Impact'. "
            "Instead of just listing tasks, use numbers (e.g., 'Increased efficiency by 20%'). "
            "Make sure your contact info and top skills are impossible to miss."
        ),
        "Hiring Manager": (
            "🛠️ **Hiring Manager's View:** Your technical stack is relevant, but I need to see "
            "the 'Depth' of your projects. Mention the challenges you faced and how you solved them. "
            "I'm looking for a problem-solver, not just a coder."
        ),
        "CTO": (
            "🚀 **CTO's View:** I'm looking for architectural understanding and scalability. "
            "Your tech knowledge is good, but explain *why* you chose a particular database or framework. "
            "Show me that you understand the big picture of the product."
        ),
        "ATS Bot": (
            "🤖 **ATS Bot's View:** Your formatting is safe, but keyword density is key. "
            "Ensure you've used exact terms from the Job Description (JD) so my filters "
            "rank you at the top of the pile."
        )
    }

    # Returns the specific feedback or a professional default message
    return persona_feedback.get(
        persona, 
        "🔍 **General Feedback:** Your resume has a solid foundation. Focus on aligning your "
        "summary with the specific role you are applying for to stand out."
    )