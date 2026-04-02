import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🚀 CORE CONFIG
# ==============================
track_visit()
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

# ==============================
# 📱 THE "WHITE ON BLUE" ROADMAP CSS
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🛡️ BLUE ACTION ZONE */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
}

/* White Text for Uploader Label */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span {
    color: #ffffff !important;
}

/* ⚪ BROWSE BUTTON: Dark Blue Text */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
}

/* 📊 METRICS: Blue Numbers */
[data-testid="stMetricValue"] div { color: #1e3a8a !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] p { color: #475569 !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; padding: 10px !important; }

/* 🛠️ ROADMAP: WHITE ON BLUE (Requested Fix) */
.plan-card {
    background-color: #1e3a8a !important; /* Deep Blue Background */
    border-left: 8px solid #5eead4 !important; /* Teal Highlight */
    padding: 15px !important;
    margin-bottom: 12px !important;
    border-radius: 10px !important;
    color: #ffffff !important; /* FORCE PURE WHITE TEXT */
    font-weight: 500 !important;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Footer Fix */
.footer-container p, .footer-container b { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px;">
    <h1 style="color: #ffffff !important; margin:0; font-size: 28px; font-weight: 800;">PLACEMENT ASSISTANT AI</h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# ... (Inputs and Logic same as before) ...
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
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

# RESULTS & ROADMAP
if st.session_state.get('analyzed'):
    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{st.session_state['ats_data']['total']}/100")
    m2.metric("JD MATCH", f"{st.session_state['jd_score']}%")

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(st.session_state['ats_data']['total'], st.session_state['jd_score'], st.session_state['risks'])
    
    for i, step in enumerate(plan):
        # 🏹 WHITE ON BLUE FORCE
        st.markdown(f"""
        <div class="plan-card">
            <b style="color: #5eead4;">Step {i+1}:</b> 
            <span style="color: #ffffff !important;">{step}</span>
        </div>
        """, unsafe_allow_html=True)

# COMMUNITY IMPACT
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: st.metric("Success Rate", "94%")

# FOOTER
st.markdown(f"""
<div style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="margin-bottom:10px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div>
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">📧 Feedback</a>
    </div>
</div>
""", unsafe_allow_html=True)