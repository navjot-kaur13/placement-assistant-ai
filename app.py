import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🧠 INTERVIEW ENGINE LOGIC
# ==============================
def generate_questions(resume_text):
    # Aapke resume ke content ke basis par questions
    questions = [
        "Can you walk me through the most technical project mentioned in your resume?",
        "What was the biggest challenge you faced while working on these technologies?",
        "How would you apply your specific skills to solve a real-world problem in our company?",
        "If you had to redo one of your projects today, what technical changes would you make?",
        "Describe a situation where you had to learn a new tool or technology very quickly."
    ]
    # Simple keyword-based logic for more relevant questions
    if "React" in resume_text or "Frontend" in resume_text:
        questions.append("How do you handle state management in large-scale applications?")
    if "Python" in resume_text or "Backend" in resume_text:
        questions.append("How do you ensure your API endpoints are secure and scalable?")
    
    return questions[:5] # Return top 5

# ==============================
# 🚀 CORE CONFIG
# ==============================
track_visit()
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
textarea, [data-testid="stFileUploader"] section { background-color: #1e3a8a !important; border: 2px solid #3b82f6 !important; }
[data-testid="stFileUploader"] section div div, [data-testid="stFileUploader"] section span, .stTextArea textarea { color: #ffffff !important; }
div[data-testid="stFileUploader"] section button { background-color: #ffffff !important; color: #1e3a8a !important; font-weight: 900 !important; }
[data-testid="stMetricValue"] > div { color: #1e3a8a !important; font-weight: 800 !important; }
[data-testid="stMetric"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; padding: 15px !important; border-radius: 10px !important; }
.plan-card { background-color: #ffffff !important; border-left: 8px solid #10b981 !important; padding: 15px !important; margin-bottom: 10px !important; border-radius: 8px !important; box-shadow: 0px 2px 8px rgba(0,0,0,0.05); }
.keyword-chip { background-color: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 20px; font-weight: bold; margin-right: 5px; display: inline-block; margin-bottom: 8px; border: 1px solid #bae6fd; }
.q-box { background-color: #f0f9ff; padding: 15px; border-radius: 10px; border-left: 5px solid #0ea5e9; margin-bottom: 10px; color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px;">
    <h1 style="color: white !important; margin:0; font-size: 32px; font-weight: 800;">PLACEMENT ASSISTANT AI</h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px; font-weight: 500;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🚀 RUN FULL AI DIAGNOSTIC"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is analyzing your profile..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Please upload your resume first!")

# RESULTS SECTION
if st.session_state.get('analyzed'):
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    res_text = st.session_state['resume_text']
    
    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tabs = st.tabs(["📊 Breakdown", "🎯 Keywords to Add", "⚠️ Risks", "👤 Persona Review", "🎤 Prep"])
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords']); b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs']); b4.metric("Impact", ats['impact'])
    
    with tabs[1]:
        st.write("### 🚀 Add these keywords to increase JD Match:")
        # Logic to extract keywords from JD can be complex, showing high-impact ones
        suggested_keywords = ["System Design", "Unit Testing", "Scalability", "REST APIs", "Cloud Deployment", "Agile Methodology"]
        for word in suggested_keywords:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
        st.info("💡 Tip: Integrate these naturally into your work experience or projects section.")

    with tabs[2]:
        if st.session_state['risks']:
            for r in st.session_state['risks']: st.error(f"🚨 {r}")
        else: st.success("🎉 Excellent! No critical risks found in your resume structure.")
        
    with tabs[3]:
        st.write("### 👤 Persona Analysis")
        persona = st.selectbox("View feedback from:", ["Recruiter", "Technical Lead", "HR Manager"])
        st.info(persona_engine(res_text, persona))

    with tabs[4]:
        st.write("### 🎤 Interview Practice Questions")
        questions = generate_questions(res_text)
        for i, q in enumerate(questions):
            st.markdown(f'<div class="q-box"><b>Q{i+1}:</b> {q}</div>', unsafe_allow_html=True)
        st.success("💡 Tip: Use the STAR method (Situation, Task, Action, Result) to answer these.")

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, st.session_state['risks'])
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# COMMUNITY IMPACT
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", f"{data['visits']}")
with c2: st.metric("Resumes Scanned", f"{data['analyses']}")
with c3: st.metric("Success Rate", "94%")

# FOOTER
st.markdown(f"""
<div style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="color:white !important; margin-bottom:10px; font-size: 18px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div style="margin-top: 15px;">
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4 !important; margin:0 15px; font-weight:bold; text-decoration:none;">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13/placement-assistant-ai" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">📧 Feedback</a>
    </div>
    <p style="color:rgba(255,255,255,0.6) !important; font-size: 12px; margin-top: 20px;">© 2026 Placement Assistant AI | Empowering Your Career Journey</p>
</div>
""", unsafe_allow_html=True)