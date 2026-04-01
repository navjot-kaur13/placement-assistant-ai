import streamlit as st

# ==============================
# Backend Imports
# ==============================
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan

# 🔥 Analytics
from analytics import track_visit, track_analysis, load_data

# ==============================
# Track Visit
# ==============================
track_visit()

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Placement Assistant AI", layout="wide")

# ==============================
# 🎨 UI Styling
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #c7d2fe, #e0f2fe);
}
.block-container {
    padding-top: 5rem !important;
    padding-bottom: 2rem;
}
.stMetric, .stAlert, div[data-testid="stExpander"], .stTabs {
    background-color: white !important;
    color: #1e293b !important;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.3);
    margin-bottom: 20px;
}
[data-testid="stMetricValue"] { color: #1d4ed8 !important; }
h1, h2, h3 { color: #1e1b4b !important; margin-bottom: 1.5rem !important; }
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white !important;
    border-radius: 10px;
    height: 3.5em;
    width: 100%;
    font-weight: bold;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: linear-gradient(135deg, #2563eb, #4f46e5); padding: 50px; border-radius: 20px; color: white; text-align: center; margin-bottom: 35px;">
    <h1 style="color: white !important;">🚀 Placement Assistant AI</h1>
    <p style="font-size:18px;">Get ATS score, job match & personalized improvement plan instantly</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# INPUT SECTION
# ==============================
col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")
with col2:
    st.markdown("##### 📌 Paste Job Description")
    jd_text = st.text_area("", height=150, placeholder="Paste requirements here...", label_visibility="collapsed")

# ==============================
# ANALYZE LOGIC
# ==============================
if st.button("🚀 Analyze Resume"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume first")
    else:
        track_analysis()
        with st.spinner("Analyzing..."):
            resume_text = extract_text(uploaded_file)
            # Store in session state so persona switching works
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True

if st.session_state.get('analyzed'):
    resume_text = st.session_state['resume_text']
    ats_data = st.session_state['ats_data']
    ats_score = ats_data["total"]
    jd_score = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("## 📊 Your Resume Insights")
    c1, c2 = st.columns(2)
    c1.metric("ATS Score", f"{ats_score}/100")
    c2.metric("JD Match", f"{jd_score}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 ATS Breakdown", "🎯 JD Match", "⚠️ Risks", "💡 Expert Feedback"])

    with tab1:
        st.progress(ats_score / 100)
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats_data["keywords"])
        b2.metric("Structure", ats_data["sections"])
        b3.metric("Verbs", ats_data["verbs"])
        b4.metric("Impact", ats_data["impact"])

    with tab2:
        if jd_text.strip():
            st.progress(jd_score / 100)
            st.write(f"Match Score: {jd_score}%")
        else:
            st.info("Paste JD to see match.")

    with tab3:
        if risks:
            for r in risks: st.warning(r)
        else: st.success("No risks found!")

    with tab4:
        # Selection triggers a rerun, and since we use session_state, it stays!
        persona_choice = st.selectbox("Choose a Perspective", ["Recruiter", "Hiring Manager", "CTO"], key="p_select")
        feedback = persona_engine(resume_text, persona_choice)
        st.info(feedback)

    st.markdown("### 🚀 Improvement Plan")
    plan = generate_plan(ats_score, jd_score, risks)
    for step in plan:
        st.markdown(f"✅ {step}")

# ==============================
# ANALYTICS
# ==============================
data = load_data()
st.markdown("---")
st.write(f"Visits: {data['visits']} | Analyzed: {data['analyses']}")