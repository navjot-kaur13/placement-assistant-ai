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
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

# ==============================
# 📱 SUPER FORCE CSS (COLOR & TABS FIX)
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🛡️ JD & UPLOADER: Force White Text and Blue Background */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
}

/* Force text inside JD box to be WHITE */
.stTextArea textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Force White Text for Uploader */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section p {
    color: #ffffff !important;
}

/* Browse Button Fix */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
}

/* 🚀 RUN BUTTON */
div.stButton > button {
    background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%) !important;
    color: white !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    height: 50px !important;
}

/* Roadmap & Result Cards */
.plan-card {
    background: white !important;
    border-left: 8px solid #10b981 !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
    border-radius: 8px !important;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Metrics Fix */
[data-testid="stMetricValue"] div { color: #1e3a8a !important; font-weight: 800 !important; }
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px;">
    <div style="font-size:30px;">🏹</div>
    <h1 style="color: #ffffff !important; margin:0; font-size: 32px; font-weight: 800;">PLACEMENT ASSISTANT AI</h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px; font-weight: 500;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=150, placeholder="Paste JD here...", label_visibility="collapsed")

# RUN BUTTON LOGIC
if st.button("🚀 RUN FULL AI DIAGNOSTIC"):
    if uploaded_file:
        track_analysis()
        with st.spinner("Analyzing profile..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Upload resume first!")

# RESULTS SECTION (FULL RESTORE)
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    # RESTORING ALL TABS
    tabs = st.tabs(["📊 Breakdown", "🎯 Keywords", "⚠️ Risks", "💡 Advice", "🎤 Interview Prep"])
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords']); b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs']); b4.metric("Impact", ats['impact'])
    
    with tabs[1]:
        st.write("**Include these keywords to improve matching:**")
        for word in ["React.js", "Python", "SQL", "Leadership", "Agile"]:
            st.markdown(f'<span style="background:#dcfce7; color:#166534; padding:5px 12px; border-radius:20px; margin:5px; font-weight:bold; border:1px solid #166534;">{word}</span>', unsafe_allow_html=True)
            
    with tabs[2]:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected!")

    with tabs[3]:
        p = st.selectbox("View Advice From:", ["Recruiter", "Hiring Manager", "CTO"], key="advisor_sel")
        st.info(persona_engine(res_text, p))

    with tabs[4]:
        st.write("### 🎤 Practice These Questions")
        qs = generate_questions(res_text)
        for i, q in enumerate(qs): st.markdown(f"**Q{i+1}:** {q}")

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# ANALYTICS
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
col1, col2, col3 = st.columns(3)
with col1: st.metric("Global Visitors", data['visits'])
with col2: st.metric("Resumes Scanned", data['analyses'])
with col3: st.metric("Success Rate", "94%")

# FOOTER
st.markdown(f"""
<div style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="color: #ffffff !important; margin-bottom:10px; font-weight: bold;">Built with ❤️ by Navjot Kaur</p>
    <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4 !important; margin:0 15px; font-weight:bold; text-decoration:none;">🔗 LinkedIn</a>
    <a href="https://github.com/navjot-kaur13/placement-assistant-ai" style="color:#5eead4 !important; margin:0 15px; font-weight:bold; text-decoration:none;">💻 GitHub</a>
    <a href="mailto:kaur21navjot@gmail.com" style="color:#5eead4 !important; margin:0 15px; font-weight:bold; text-decoration:none;">📧 Feedback</a>
</div>
""", unsafe_allow_html=True)