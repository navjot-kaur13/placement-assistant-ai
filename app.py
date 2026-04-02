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
    questions = [
        "Can you walk me through the most technical project mentioned in your resume?",
        "What was the biggest challenge you faced while working on your projects?",
        "How would you apply your specific skills to solve a real-world problem here?",
        "If you had to redo one of your projects today, what would you change?",
        "Describe a situation where you had to learn a new technology quickly."
    ]
    if "React" in resume_text or "Frontend" in resume_text:
        questions.append("How do you manage state in a large-scale frontend application?")
    if "Python" in resume_text or "Backend" in resume_text:
        questions.append("How would you handle slow API responses in a backend system?")
    return questions[:5]

# ==============================
# 🚀 CORE LOGIC & CONFIG
# ==============================
track_visit()
st.set_page_config(page_title="Placement AI | Career Copilot", page_icon="🎯", layout="wide")

# ==============================
# 📱 ADVANCED CSS (MOBILE FIX + FOOTER)
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

/* 🚨 DARK MODE OVERWRITE */
textarea, [data-testid="stFileUploader"], .stTextArea textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cbd5e1 !important;
    -webkit-text-fill-color: #000000 !important;
}

.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 10px solid #10b981 !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
    border-radius: 10px !important;
}

/* Professional Footer Styling */
.footer-container {
    background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
    padding: 40px 20px;
    border-radius: 25px 25px 0 0;
    color: white !important;
    text-align: center;
    margin-top: 60px;
    box-shadow: 0px -10px 30px rgba(30, 58, 138, 0.1);
}
.footer-link {
    color: #5eead4 !important;
    text-decoration: none;
    font-weight: bold;
    margin: 0 15px;
    font-size: 16px;
}
.footer-link:hover { text-decoration: underline; }

.hero-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); 
    padding: 30px 20px; 
    border-radius: 25px; 
    color: white !important; 
    text-align: center; 
    margin-bottom: 30px; 
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div class="hero-container">
    <div style="font-size:35px;">🏹</div>
    <h1 style="color: white !important; margin:0;">PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span></h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is analyzing your career path..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Please upload your resume first!")

# RESULTS
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tabs = st.tabs(["📊 Breakdown", "🎯 Keywords", "⚠️ Risks", "💡 Advice", "🎤 Interview Prep"])
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords']); b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs']); b4.metric("Impact", ats['impact'])
    
    with tabs[1]:
        st.write("Top Keywords:")
        for word in ["React.js", "Python", "SQL", "Leadership", "Agile"]:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
            
    with tabs[2]:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No risks!")

    with tabs[3]:
        p = st.selectbox("Advisor:", ["Recruiter", "Hiring Manager", "CTO"], key="adv_box")
        st.info(persona_engine(res_text, p))
        
    with tabs[4]:
        st.write("### 🎤 Practice Questions")
        qs = generate_questions(res_text)
        for i, q in enumerate(qs): st.markdown(f"**Q{i+1}:** {q}")

    st.markdown("<br>---", unsafe_allow_html=True)
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# ANALYTICS
st.markdown("<br><br>---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: st.metric("Success Rate", "94%")

# ==============================
# 🏆 STEP 3: PROFESSIONAL FOOTER (UPDATED)
# ==============================
st.markdown(f"""
<div class="footer-container">
    <p style="margin-bottom: 10px; font-size: 18px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div style="margin-top: 20px;">
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" class="footer-link" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13/placement-assistant-ai" class="footer-link" target="_blank">💻 GitHub Project</a>
        <a href="mailto:kaur21navjot@gmail.com" class="footer-link">📧 Feedback</a>
    </div>
    <p style="font-size: 12px; margin-top: 25px; opacity: 0.8;">© 2026 Placement Assistant AI | Empowering Careers with AI</p>
</div>
""", unsafe_allow_html=True)