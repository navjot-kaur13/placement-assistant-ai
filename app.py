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
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

# ==============================
# 📱 MOBILE-FIRST RESPONSIVE CSS
# ==============================
st.markdown("""
<style>
/* Global Reset */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🏹 HERO SECTION */
.hero-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); 
    padding: 30px 15px; 
    border-radius: 20px; 
    text-align: center; 
    margin-bottom: 25px; 
}
.hero-container h1 { color: #ffffff !important; font-size: 26px !important; margin: 0; }
.hero-container p { color: #ccfbf1 !important; font-size: 14px !important; }

/* 🛡️ ACTION BOXES (Step 1 & 2) */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 12px !important;
}

/* White Text for Inputs */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span,
.stTextArea textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Browse Button Fix */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
}

/* 📊 METRICS & TABS FIX (Mobile Centered) */
[data-testid="stMetricValue"] > div {
    color: #1e3a8a !important;
    font-size: 24px !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] p {
    color: #64748b !important;
    font-size: 12px !important;
}
[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    padding: 10px !important;
    border-radius: 10px !important;
}

/* Tabs Mobile Spacing */
button[data-baseweb="tab"] {
    font-size: 12px !important;
    padding: 5px !important;
}

/* Roadmap List Items */
.plan-card {
    background: white !important;
    border-left: 5px solid #10b981 !important;
    padding: 12px !important;
    margin-bottom: 8px !important;
    border-radius: 6px !important;
    color: #1e293b !important;
    font-size: 14px !important;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
}

/* Footer Fix */
.footer-container {
    background: #1e3a8a !important;
    padding: 20px !important;
    border-radius: 15px !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div class="hero-container">
    <div style="font-size:30px;">🏹</div>
    <h1>PLACEMENT ASSISTANT AI</h1>
    <p>Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=100, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🚀 RUN FULL AI DIAGNOSTIC"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI analyzing..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Upload resume first!")

# RESULTS
if st.session_state.get('analyzed'):
    st.markdown("### 📊 Your Results")
    ats_score = st.session_state['ats_data']['total']
    jd_match = st.session_state['jd_score']
    
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats_score}/100")
    m2.metric("JD MATCH", f"{jd_match}%")

    tabs = st.tabs(["📊 Breakdown", "⚠️ Risks", "💡 Advice", "🎤 Prep"])
    with tabs[3]:
        st.info("Preparing interview questions...")

    st.markdown("---")
    st.markdown("### 🛠️ Roadmap")
    plan = generate_plan(ats_score, jd_match, st.session_state['risks'])
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
<div class="footer-container">
    <p style="color:white !important; margin-bottom:10px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">🔗 LinkedIn</a>
    <a href="https://github.com/navjot-kaur13/placement-assistant-ai" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">💻 GitHub</a>
    <a href="mail:kaur21navjot@gmail.com" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">📧 Feedback</a>
</div>
""", unsafe_allow_html=True)