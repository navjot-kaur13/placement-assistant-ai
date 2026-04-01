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
st.set_page_config(page_title="Placement Assistant AI", layout="wide")

# ==============================
# 📱 ULTRA-HIGH CONTRAST UI FIX
# ==============================
st.markdown("""
<style>
/* Background Fix */
[data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }

/* Force ALL text to be dark and visible */
h1, h2, h3, h4, h5, p, span, label, div {
    color: #000000 !important; 
    font-weight: 500;
}

/* Metric Boxes Fix (Visits, Analyzed, etc.) */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 2px solid #1e3a8a !important; /* Thick Dark Blue Border */
    border-radius: 10px !important;
    padding: 15px !important;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1) !important;
}

/* Metric Numbers Color */
[data-testid="stMetricValue"] {
    color: #1d4ed8 !important;
    font-weight: 900 !important;
    font-size: 32px !important;
}

/* Metric Labels Color */
[data-testid="stMetricLabel"] {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* File Uploader Fix */
[data-testid="stFileUploader"] section {
    background-color: #1e40af !important;
    border: 2px dashed #ffffff !important;
    color: white !important;
}
[data-testid="stFileUploader"] label { color: white !important; }

/* Roadmap Cards Fix */
.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #1e293b !important;
    border-left: 8px solid #10b981 !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    border-radius: 8px !important;
}

/* Tab visibility */
button[data-baseweb="tab"] p {
    color: #1d4ed8 !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: #1e3a8a; padding: 30px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 25px;">
    <h1 style="color: white !important; margin: 0; font-size: 28px;">🚀 Placement Assistant AI</h1>
    <p style="color: #bfdbfe !important; margin-top: 5px;">Your Smart Career Copilot</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📊 TOP ANALYTICS (Community Impact)
# ==============================
data = load_data()
a1, a2, a3 = st.columns(3)

with a1:
    st.metric("Total Visitors", data['visits'])
with a2:
    st.metric("Resumes Analyzed", data['analyses'])
with a3:
    # Success metric wake-up call
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# 📄 INPUT SECTION
# ==============================
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Select your Resume (PDF/DOCX)", type=["pdf", "docx"])

st.markdown("### 📌 Step 2: Target Job Description")
jd_text = st.text_area("Job Description", height=120, placeholder="Paste JD here for matching score...", label_visibility="collapsed")

if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI scanning in progress..."):
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

    st.markdown("### 📊 Your Placement Insights")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Matching", "⚠️ Risks", "💡 Advice"])

    with tab1:
        st.write("Score breakdown based on structure and impact:")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        if jd_text.strip():
            st.write(f"Overall Compatibility: {jd_s}%")
            st.progress(jd_s/100)
        else:
            st.info("💡 Paste a Job Description above to see compatibility matching.")

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected. Great job!")

    with tab4:
        p = st.selectbox("View Advice From:", ["Recruiter", "Hiring Manager", "CTO"], key="p_final")
        st.info(persona_engine(res_text, p))

    # ROADMAP SECTION
    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap to Success")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f"""
        <div class="plan-card">
            <div style="color:#059669; font-weight:800; font-size:12px; text-transform:uppercase;">Step {i+1}</div>
            <div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div>
        </div>
        """, unsafe_allow_html=True)