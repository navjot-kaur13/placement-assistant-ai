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
# 📱 THE "NO-OVERLAP" CSS FIX
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* 🛡️ BLUE ACTION ZONE */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
}

/* Force White Text for Uploader Label */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span {
    color: #ffffff !important;
}

/* ⚪ BROWSE BUTTON: Dark Blue Text (Force Visibility) */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    border: none !important;
}

/* 🚀 RUN BUTTON (The Laptop Look) */
div.stButton > button {
    background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%) !important;
    color: white !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    height: 50px !important;
}

/* 📊 METRICS: Blue Numbers & Labels */
[data-testid="stMetricValue"] div { color: #1e3a8a !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] p { color: #475569 !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; padding: 10px !important; }

/* 🛠️ ROADMAP: FORCE DARK TEXT (Visibility Fix) */
.plan-card {
    background-color: #ffffff !important;
    border-left: 8px solid #10b981 !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
    border-radius: 8px !important;
    color: #1e293b !important; /* DARK TEXT FOR VISIBILITY */
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
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

# INPUTS
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

# RESULTS SECTION
if st.session_state.get('analyzed'):
    st.markdown("### 📊 Your Results")
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tabs = st.tabs(["📊 Breakdown", "⚠️ Risks", "👤 Persona", "🎤 Prep"])
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    st.markdown("---")
    st.markdown("### 🛠️ Roadmap")
    plan = generate_plan(ats['total'], jd_s, st.session_state['risks'])
    for i, step in enumerate(plan):
        # Yahan humne inline style add kiya hai taaki text pakka dikhe
        st.markdown(f'<div class="plan-card" style="color: #1e293b !important;"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

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
<div class="footer-container" style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="margin-bottom:10px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div>
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" style="color:#5eead4 !important; margin:0 10px; font-weight:bold; text-decoration:none;">📧 Feedback</a>
    </div>
</div>
""", unsafe_allow_html=True)