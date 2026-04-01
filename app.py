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
# 🎨 Updated UI Styling
# ==============================
st.markdown("""
<style>
/* Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #c7d2fe, #e0f2fe);
}

/* Navbar gap and Top Spacing */
.block-container {
    padding-top: 5rem !important; /* Increases space at the top */
    padding-bottom: 2rem;
}

/* Card Styling for Visibility */
.stMetric, .stAlert, div[data-testid="stExpander"], .stTabs {
    background-color: white !important;
    color: #1e293b !important; /* Dark blue-grey text */
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.3);
    margin-bottom: 20px;
}

/* Metric text color fix */
[data-testid="stMetricValue"] {
    color: #1d4ed8 !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
}

/* Heading color fix */
h1, h2, h3 {
    color: #1e1b4b !important; /* Deep Navy for contrast */
    margin-bottom: 1.5rem !important;
}

/* General Text spacing and color */
p, span, label {
    color: #334155 !important;
    font-weight: 500;
}

.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white !important;
    border-radius: 10px;
    height: 3.5em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4);
    transform: translateY(-2px);
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
    padding: 50px 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.3);
">
    <h1 style="color: white !important; margin: 0;">🚀 Placement Assistant AI</h1>
    <p style="font-size:18px; color: #e0e7ff !important; margin-top: 10px;">
        Get ATS score, job match & personalized improvement plan instantly
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# FEATURES
# ==============================
st.markdown("### ⚡ What You Get")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background:white; padding:20px; border-radius:15px; border-left: 5px solid #2563eb;">
    <h4 style="margin:0;">📊 Smart ATS Analysis</h4>
    <p style="font-size:14px; margin:0;">Detailed scoring with breakdown</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background:white; padding:20px; border-radius:15px; border-left: 5px solid #2563eb;">
    <h4 style="margin:0;">🎯 Job Matching</h4>
    <p style="font-size:14px; margin:0;">Match resume with job descriptions</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background:white; padding:20px; border-radius:15px; border-left: 5px solid #2563eb;">
    <h4 style="margin:0;">🚀 Improvement Plan</h4>
    <p style="font-size:14px; margin:0;">AI-powered improvement steps</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# TRUST
# ==============================
st.markdown("""
<div style="text-align:center; margin:30px 0;">
<p style="color:#475569 !important; font-style: italic;">Trusted by students to improve resumes 🚀</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# INPUT SECTION
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")

with col2:
    st.markdown("##### 📌 Paste Job Description")
    jd_text = st.text_area("", height=150, placeholder="Paste the job requirements here...", label_visibility="collapsed")

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
                st.error("Status: Needs Improvement")
            elif ats_score < 70:
                st.warning("Status: Average")
            elif ats_score < 85:
                st.info("Status: Good")
            else:
                st.success("Status: Excellent")

        with c2:
            st.metric("JD Match", f"{jd_score}%")

        st.markdown("---")

        # TABS
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
                st.metric("Match Score", f"{jd_score}%")
            else:
                st.info("Please paste a Job Description in the input section above to see the match score.")

        with tab3:
            if risks:
                for r in risks:
                    st.warning(r)
            else:
                st.success("No major structural risks found. Your resume looks clean!")

        with tab4:
            persona = st.selectbox("Choose a Perspective", ["Recruiter", "Hiring Manager", "CTO"])
            st.markdown(f"**Insight from a {persona}:**")
            st.info(persona_engine(resume_text, persona))

        # PLAN
        st.markdown("### 🚀 Improvement Plan")
        plan = generate_plan(ats_score, jd_score, risks)
        for step in plan:
            st.markdown(f"""
            <div style="background:white; padding:10px 15px; border-radius:10px; margin-bottom:10px; border-left:4px solid #10b981;">
            ✅ {step}
            </div>
            """, unsafe_allow_html=True)

# ==============================
# 📈 ANALYTICS DISPLAY
# ==============================
data = load_data()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 📈 Usage Analytics")

a1, a2 = st.columns(2)
a1.markdown(f"""
<div style="background:#f8fafc; padding:20px; border-radius:15px; text-align:center;">
    <h2 style="margin:0; color:#2563eb;">{data['visits']}</h2>
    <p style="margin:0; color:#64748b;">Total Visits</p>
</div>
""", unsafe_allow_html=True)

a2.markdown(f"""
<div style="background:#f8fafc; padding:20px; border-radius:15px; text-align:center;">
    <h2 style="margin:0; color:#2563eb;">{data['analyses']}</h2>
    <p style="margin:0; color:#64748b;">Resumes Analyzed</p>
</div>
""", unsafe_allow_html=True)