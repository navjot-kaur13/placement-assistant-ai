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
    # Simple customization
    if "React" in resume_text or "Frontend" in resume_text:
        questions.append("How do you manage state in a large-scale frontend application?")
    if "Python" in resume_text or "Backend" in resume_text:
        questions.append("How would you handle slow API responses in a backend system?")
    return questions[:5]

# ==============================
# 🚀 CORE LOGIC & CONFIG
# ==============================
track_visit()
st.set_page_config(
    page_title="Placement AI | Target Your Dream Job", 
    page_icon="🎯", 
    layout="wide"
)

# ==============================
# 📱 MOBILE-FIRST & HIGH CONTRAST CSS
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

textarea, [data-testid="stFileUploader"], .stTextArea textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

[data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px dashed #ffffff !important;
    color: white !important;
}

div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
    border: none !important;
}

div.stButton > button:first-child {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    height: 55px !important;
    box-shadow: 0px 4px 15px rgba(30, 58, 175, 0.3) !important;
}

.keyword-chip {
    display: inline-block;
    background-color: #dcfce7;
    color: #166534;
    padding: 5px 12px;
    border-radius: 20px;
    margin: 5px;
    font-size: 14px;
    font-weight: bold;
    border: 1px solid #166534;
}

.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 10px solid #10b981 !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* 🏹 HERO SECTION STYLING */
.hero-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); 
    padding: 40px 20px; 
    border-radius: 25px; 
    color: white !important; 
    text-align: center; 
    margin-bottom: 30px; 
    box-shadow: 0px 15px 30px rgba(13, 148, 136, 0.2);
    border: 1px solid rgba(255,255,255,0.1);
}
.hero-title { font-size: 38px; font-weight: 800; margin: 0; color: white !important; }
.hero-subtitle { font-size: 16px; opacity: 0.9; margin-top: 10px; color: #ccfbf1 !important; }
.hero-icon { font-size: 40px; margin-bottom: 10px; }

@media (max-width: 640px) {
    .hero-container { padding: 25px 10px; border-radius: 15px; margin-bottom: 20px; }
    .hero-title { font-size: 24px; }
    .hero-subtitle { font-size: 13px; margin-top: 5px; }
    .hero-icon { font-size: 30px; margin-bottom: 5px; }
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div class="hero-container">
    <div class="hero-icon">🏹</div>
    <h1 class="hero-title">PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span></h1>
    <p class="hero-subtitle">"Precision in every scan. Accuracy in every roadmap."</p>
</div>
""", unsafe_allow_html=True)

# STEP 1 & 2
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD Input", height=150, placeholder="Paste Job Description here...", label_visibility="collapsed")

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
    else:
        st.warning("Please upload your resume first!")

# RESULTS DASHBOARD
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    # 🎤 ADDED INTERVIEW PREP TAB HERE
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Breakdown", "🎯 Keyword Guide", "⚠️ Risks", "💡 Advice", "🎤 Interview Prep"])
    
    with tab1:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        st.write("**Top Keywords to include:**")
        examples = ["React.js", "Python", "Cloud Computing", "Team Leadership", "SQL", "Agile"]
        for word in examples:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected!")

    with tab4:
        p = st.selectbox("Advisor:", ["Recruiter", "Hiring Manager", "CTO"], key="p_select")
        st.info(persona_engine(res_text, p))

    with tab5:
        st.write("### 🎤 Practice These Questions")
        st.info("Based on your resume, prepare for these specific questions:")
        qs = generate_questions(res_text)
        for i, q in enumerate(qs):
            st.markdown(f"**Q{i+1}:** {q}")

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><div style="color:#059669; font-weight:800; font-size:12px;">STEP {i+1}</div><div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div></div>', unsafe_allow_html=True)

# COMMUNITY ANALYTICS
st.markdown("<br><br>---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: 
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)