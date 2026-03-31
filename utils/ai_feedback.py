from openai import OpenAI

# 🔑 Add your API key here
client = OpenAI(api_key="YOUR_API_KEY")

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
    try:
        prompt = f"""
You are a professional resume reviewer.

Analyze the following resume insights and give clear, practical, and structured feedback.

DATA:
Skills: {skills}
Skill Depth: {skill_depths}
ATS Score: {ats_result['ats_score']}
JD Match: {jd_result['match_percentage']}
Bullet Analysis: {bullet_analysis}
Risk Flags: {risk_flags}

Give output in this format:
1. Overall evaluation
2. Key strengths
3. Major weaknesses
4. Specific improvements (actionable)
5. Final suggestion
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume coach."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating AI feedback: {str(e)}"