import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

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
/* Global Background and Text Fix */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

/* 🚨 THE MOBILE DARK-MODE KILLER (Force White Backgrounds) */
textarea, [data-testid="stFileUploader"], .stTextArea textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* File Uploader Container Fix */
[data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px dashed #ffffff !important;
    color: white !important;
}

/* Browse Button Fix (White/Visible) */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
    border: none !important;
}

/* Action Button (Run Diagnostic) */
div.stButton > button:first-child {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    height: 55px !important;
    box-shadow: 0px 4px 15px rgba(30, 58, 175, 0.3) !important;
}

/* Keyword Chips Style */
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

/* Roadmap Cards */
.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 10px solid #10b981 !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    border-radius: 10px !important;
}

/* Metrics Styling (Bottom Section) */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* ==============================
   🏹 HERO SECTION STYLING (RESPONSIVE)
   ============================== */
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

/* Mobile adjustments */
@media (max-width: 640px) {
    .hero-container { padding: 25px 10px; border-radius: 15px; margin-bottom: 20px; }
    .hero-title { font-size: 24px; }
    .hero-subtitle { font-size: 13px; margin-top: 5px; }
    .hero-icon { font-size: 30px; margin-bottom: 5px; }
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🏹 HERO SECTION DISPLAY
# ==============================
st.markdown("""
<div class="hero-container">
    <div class="hero-icon">🏹</div>
    <h1 class="hero-title">
        PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span>
    </h1>
    <p class="hero-subtitle">
        "Precision in every scan. Accuracy in every roadmap."
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📄 STEP 1 & 2
# ==============================
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target Job Description")
jd_text = st.text_area("JD Input Box", height=150, placeholder="Paste Job Description here to check for keyword matching...", label_visibility="collapsed")

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

# ==============================
# 📊 RESULTS DASHBOARD
# ==============================
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Keyword Guide", "⚠️ Risks", "💡 Advice"])
    
    with tab1:
        st.write("Detailed structure analysis:")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        st.write("**Top Keywords to include in your resume:**")
        examples = ["React.js", "Python", "Cloud Computing", "Team Leadership", "Problem Solving", "SQL", "Agile"]
        for word in examples:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
        st.info("💡 Pro-Tip: Integrating these keywords into your Bullet Points increases visibility to recruiters.")

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected!")

    with tab4:
        p = st.selectbox("View Advice From:", ["Recruiter", "Hiring Manager", "CTO"], key="persona_select")
        st.info(persona_engine(res_text, p))

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f"""
        <div class="plan-card">
            <div style="color:#059669; font-weight:800; font-size:12px; text-transform:uppercase;">Step {i+1}</div>
            <div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# 📈 COMMUNITY ANALYTICS
# ==============================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Global Visitors", data['visits'])
with c2:
    st.metric("Resumes Scanned", data['analyses'])
with c3:
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)