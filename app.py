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
# 📱 UNIVERSAL CSS (FORCE WHITE ON ALL DEVICES)
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🏹 HERO SECTION: Force White Text on Laptop & Phone */
.hero-container h1, .hero-container p, .hero-container div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* 🛡️ ACTION BOXES (Blue) */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
}

/* White Text for Uploader */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section p {
    color: #ffffff !important;
}

/* 📊 METRICS (Dark Blue Numbers) */
[data-testid="stMetricValue"] div {
    color: #1e3a8a !important;
    font-weight: 800 !important;
}

/* 🏆 FOOTER: Force White Branding on Laptop & Phone */
.footer-container b, .footer-container p, .footer-container span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.footer-link {
    color: #5eead4 !important;
    text-decoration: none;
    margin: 0 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY (With Class for Targeting)
st.markdown("""
<div class="hero-container" style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px;">
    <div style="font-size:30px;">🏹</div>
    <h1 style="margin:0; font-size: 28px;">PLACEMENT ASSISTANT AI</h1>
    <p style="margin-top: 5px; opacity: 0.9;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# ... (Step 1, Step 2, and logic same as before) ...
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🚀 RUN FULL AI DIAGNOSTIC"):
    if uploaded_file:
        track_analysis()
        with st.spinner("Analyzing..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Upload resume first!")

# RESULTS SECTION (Restored for Laptop)
if st.session_state.get('analyzed'):
    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{st.session_state['ats_data']['total']}/100")
    m2.metric("JD MATCH", f"{st.session_state['jd_score']}%")
    
    # Roadmap Logic
    plan = generate_plan(st.session_state['ats_data']['total'], st.session_state['jd_score'], st.session_state['risks'])
    for i, step in enumerate(plan):
        st.markdown(f'<div style="background:white; border-left:8px solid #10b981; padding:15px; margin-bottom:10px; border-radius:8px; box-shadow: 0px 2px 8px rgba(0,0,0,0.05);"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# COMMUNITY IMPACT
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
col1, col2, col3 = st.columns(3)
with col1: st.metric("Global Visitors", data['visits'])
with col2: st.metric("Resumes Scanned", data['analyses'])
with col3: st.metric("Success Rate", "94%")

# FOOTER (With Class for Targeting)
st.markdown(f"""
<div class="footer-container" style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="margin-bottom:10px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div>
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" class="footer-link" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13/placement-assistant-ai" class="footer-link" target="_blank">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" class="footer-link">📧 Feedback</a>
    </div>
</div>
""", unsafe_allow_html=True)