import streamlit as st

# ==============================
# Import Utility Functions
# ==============================
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="AI Resume Feedback System",
    layout="wide"
)

# ==============================
# Header Section
# ==============================
st.title("🧠 AI Resume Intelligence System")
st.write("Upload your resume and get recruiter-level insights")

# ==============================
# Input Section
# ==============================
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description here",
    height=200
)

# ==============================
# Analyze Button
# ==============================
if st.button("Analyze Resume"):

    # ---------- Validation ----------
    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume file to continue.")
    
    else:
        # ---------- Resume Extraction ----------
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text(uploaded_file)

        # ---------- Tabs Layout ----------
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 ATS Score",
            "📌 JD Match",
            "🚨 Risk Flags",
            "🎯 Persona Review"
        ])

        # ==============================
        # ATS SCORE TAB
        # ==============================
        with tab1:
            ats_score = ats_engine(resume_text)
            st.metric("ATS Compatibility Score", f"{ats_score} / 100")

        # ==============================
        # JD MATCH TAB
        # ==============================
        with tab2:
            if jd_text.strip():
                jd_score = match_jd(resume_text, jd_text)
                st.metric("JD Match Percentage", f"{jd_score} %")
            else:
                st.info("ℹ️ Paste a Job Description to calculate match score.")

        # ==============================
        # RISK FLAGS TAB
        # ==============================
        with tab3:
            risks = detect_risks(resume_text)
            if risks:
                for risk in risks:
                    st.warning(risk)
            else:
                st.success("✅ No critical resume risks detected.")

        # ==============================
        # PERSONA REVIEW TAB
        # ==============================
        with tab4:
            persona = st.selectbox(
                "Select Reviewer Persona",
                ["Recruiter", "Hiring Manager", "CTO"]
            )
            feedback = persona_engine(resume_text, persona)
            st.write(feedback)
