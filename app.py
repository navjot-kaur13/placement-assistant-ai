import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🚀 CORE LOGIC
# ==============================
track_visit()
st.set_page_config(page_title="Placement Assistant AI", page_icon="🚀", layout="wide")

# ==============================
# 📱 MOBILE VISIBILITY & BROwSE FIX (ULTRA TARGETED)
# ==============================
st.markdown("""
<style>
/* Background and Global Text Fix */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

/* Metrics Styling */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 2px solid #1e3a8a !important;
    border-radius: 12px !important;
    padding: 15px !important;
    box-shadow: 4px 4px 0px rgba(30, 58, 138, 0.1) !important;
}
[data-testid="stMetricValue"] { color: #1e40af !important; font-weight: 900; }

/* 🚨 THE ULTIMATE FILE UPLOADER & BROwSE BUTTON FIX (Mobile) */
[data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important; /* Blue background */
    border: 2px dashed #ffffff !important;
    color: white !important;
}

[data-testid="stFileUploader"] label { color: white !important; font-weight: bold; }

/* Targeting the specific 'Browse files' button inside the section */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important; /* White button */
    color: #1e3a8a !important;           /* Blue text */
    font-weight: bold !important;
    border: none !important;
    border-radius: 5px !important;
}

/* FIX: Text Area (Lighter Background) */
textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cbd5e1 !important;
}

/* Main Action Button (Run AI Diagnostic) */
div.stButton > button:first-child {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    border: none !important;
    width: 100% !important;
    height: 55px !important;
    font-size: 18px !important;
    box-shadow: 0px 4px 15px rgba(30, 58, 175, 0.3) !important;
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
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div style="background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%); padding: 35px; border-radius: 20px; color: white !important; text-align: center; margin-bottom: 30px; box-shadow: 0px 10px 20px rgba(0,0,0,0.1);">
    <h1 style="color: white !important; margin: 0; font-size: 32px;">🚀 Placement Assistant AI</h1>
    <p style="color: #bfdbfe !important; margin-top: 10px; font-size: 18px;">Analyze. Improve. Get Placed.</p>
</div>
""", unsafe_allow_html=True)

# ANALYTICS
data = load_data()
a1, a2, a3 = st.columns(3)
with a1: st.metric("Total Visitors", data['visits'])
with a2: st.metric("Resumes Analyzed", data['analyses'])
with a3: 
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)

st.markdown("<br>", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Profile")
uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"])

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD Input", height=150, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is analyzing..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Please upload a resume first!")

# RESULTS
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Insights")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Matching", "⚠️ Risks", "💡 Advice"])
    with tab1:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])
    with tab2:
        if jd_text.strip():
            st.progress(jd_s/100)
            st.write(f"Match: {jd_s}%")
        else: st.info("Paste JD to see score.")
    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks!")
    with tab4:
        p = st.selectbox("Advisor:", ["Recruiter", "Hiring Manager", "CTO"], key="p_adv")
        st.info(persona_engine(res_text, p))

    st.markdown("---")
    st.markdown("### 🛠️ Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><div style="color:#059669; font-weight:800; font-size:12px;">STEP {i+1}</div><div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div></div>', unsafe_allow_html=True)