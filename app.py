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
# 📱 SUPER FORCE CSS (NO CACHE ALLOWED)
# ==============================
st.markdown("""
<style>
/* Global Reset */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🛡️ STEP 1 & 2 ACTION ZONES */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 12px !important;
}

/* ⚪ FORCE WHITE TEXT ON UPLOADER (Text Visibility) */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span, 
[data-testid="stFileUploader"] section p {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* 📱 BROWSE FILES BUTTON (Absolute Fix) */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important; /* Blue text */
    font-weight: 900 !important;
    border: 2px solid #ffffff !important;
    opacity: 1 !important;
}

/* 🚀 RUN DIAGNOSTIC BUTTON */
div.stButton > button {
    background: #2563eb !important;
    background-image: linear-gradient(90deg, #2563eb 0%, #1e40af 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4) !important;
}

/* Footer Fix */
.footer-container {
    background: #1e3a8a !important;
    padding: 20px !important;
    border-radius: 15px !important;
    text-align: center !important;
}
.footer-container b, .footer-container p { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; color: white !important; text-align: center; margin-bottom: 25px;">
    <div style="font-size:30px;">🏹</div>
    <h1 style="color: white !important; margin:0; font-size: 28px;">PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span></h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

# RUN BUTTON
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

# RESULTS & FOOTER (Analytics included in between)
if st.session_state.get('analyzed'):
    st.markdown("### 📊 Your Results")
    st.metric("ATS SCORE", f"{st.session_state['ats_data']['total']}/100")
    # ... baki roadmap aur tabs ...

# ANALYTICS
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
st.write(f"Global Visitors: {data['visits']}")

# FOOTER
st.markdown(f"""
<div class="footer-container">
    <p><b>Built with ❤️ by Navjot Kaur</b></p>
    <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4; margin-right:10px;">LinkedIn</a>
    <a href="https://github.com/navjot-kaur13/placement-assistant-ai" style="color:#5eead4;">GitHub</a>
</div>
""", unsafe_allow_html=True)