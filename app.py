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
# Track Visit (runs on page load)
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
    padding-top: 2rem;
}
.stMetric {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
}
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}
.stProgress > div > div {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    padding: 40px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
">
    <h1>🚀 Placement Assistant AI</h1>
    <p style="font-size:18px;">
        Get ATS score, job match & personalized improvement plan instantly
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# FEATURES
# ==============================
st.markdown("### ⚡ What You Get")

col1, col2, col3 = st.columns(3)
col1.markdown("### 📊 Smart ATS Analysis\nDetailed scoring with breakdown")
col2.markdown("### 🎯 Job Matching\nMatch resume with job descriptions")
col3.markdown("### 🚀 Improvement Plan\nAI-powered improvement steps")

# ==============================
# TRUST
# ==============================
st.markdown("""
<div style="text-align:center; margin:20px;">
<p style="color:#555;">Trusted by students to improve resumes 🚀</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# INPUT
# ==============================
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

with col2:
    jd_text = st.text_area("📌 Paste Job Description", height=150)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# ANALYZE
# ==============================
if st.button("🚀 Analyze Resume"):

    track_analysis()  # 🔥 TRACK USAGE

    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume first")

    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text(uploaded_file)

        ats_data = ats_engine(resume_text)
        ats_score = ats_data["total"]

        jd_score = match_jd(resume_text, jd_text) if jd_text.strip() else 0
        risks = detect_risks(resume_text)

        st.success("✅ Analysis Complete! Here’s how to improve your resume 🚀")

        # DASHBOARD
        st.markdown("## 📊 Your Resume Insights")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("ATS Score", f"{ats_score}/100")

            if ats_score < 50:
                st.markdown("<p style='color:red;'>Needs Improvement</p>", unsafe_allow_html=True)
            elif ats_score < 70:
                st.markdown("<p style='color:orange;'>Average</p>", unsafe_allow_html=True)
            elif ats_score < 85:
                st.markdown("<p style='color:#1d4ed8;'>Good</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:green;'>Excellent</p>", unsafe_allow_html=True)

        with c2:
            st.metric("JD Match", f"{jd_score}%")

        st.markdown("---")

        # TABS
        tab1, tab2, tab3, tab4 = st.tabs(["ATS", "JD Match", "Risks", "Feedback"])

        with tab1:
            st.progress(ats_score / 100)
            st.metric("Score", f"{ats_score}/100")

            st.markdown("### 📊 Breakdown")

            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Keywords", ats_data["keywords"])
            b2.metric("Structure", ats_data["sections"])
            b3.metric("Verbs", ats_data["verbs"])
            b4.metric("Impact", ats_data["impact"])

        with tab2:
            if jd_text.strip():
                st.progress(jd_score / 100)
                st.metric("Match", f"{jd_score}%")
            else:
                st.info("Paste job description")

        with tab3:
            if risks:
                for r in risks:
                    st.warning(r)
            else:
                st.success("No issues found")

        with tab4:
            persona = st.selectbox("Perspective", ["Recruiter", "Hiring Manager", "CTO"])
            st.info(persona_engine(resume_text, persona))

        # PLAN
        st.markdown("### 🚀 Improvement Plan")
        plan = generate_plan(ats_score, jd_score, risks)
        for step in plan:
            st.write(f"✅ {step}")

# ==============================
# 📈 ANALYTICS DISPLAY
# ==============================
data = load_data()

st.markdown("---")
st.markdown("### 📈 Usage Analytics")

st.write(f"👀 Total Visits: {data['visits']}")
st.write(f"📊 Total Analyses: {data['analyses']}")