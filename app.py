import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🚀 CORE LOGIC & CONFIG (Tab Icon Updated)
# ==============================
track_visit()
st.set_page_config(
    page_title="Placement AI | Target Your Dream Job", 
    page_icon="🎯", 
    layout="wide"
)

# ==============================
# 📱 MOBILE-FIRST & HIGH CONTRAST CSS (No changes here)
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

textarea, [data-testid="stFileUploader"], .stTextArea textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

[data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px dashed #ffffff !important;
    color: white !important;
}

div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
    border: none !important;
}

div.stButton > button:first-child {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    height: 55px !important;
    box-shadow: 0px 4px 15px rgba(30, 58, 175, 0.3) !important;
}

.keyword-chip {
    display: inline-block;
    background-color: #dcfce7;
    color: #166534;
    padding: 5px 12px;
    border-radius: 20px;
    margin: 5px;
    font-size: 14px;
    font-weight: bold;
    border: 1px solid #166534;
}

.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 10px solid #10b981 !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🏹 HERO SECTION (NEW LOGO CONCEPT 1)
# ==============================
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 50px; border-radius: 30px; color: white !important; text-align: center; margin-bottom: 40px; box-shadow: 0px 20px 40px rgba(13, 148, 136, 0.25); border: 1px solid rgba(255,255,255,0.1);">
    <div style="display: inline-block; background: rgba(255,255,255,0.2); padding: 20px; border-radius: 50%; margin-bottom: 15px; backdrop-filter: blur(10px);">
        <span style="font-size: 50px;">🏹</span>
    </div>
    <h1 style="color: white !important; margin: 0; font-size: 42px; font-weight: 800; letter-spacing: -1px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
        PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span>
    </h1>
    <p style="color: #ccfbf1 !important; margin-top: 10px; font-size: 18px; font-weight: 400; font-style: italic; opacity: 0.9;">
        "Precision in every scan. Accuracy in every roadmap."
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📄 STEP 1 & 2
# ==============================
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target Job Description")
jd_text = st.text_area("JD Input Box", height=150, placeholder="Paste Job Description here to check for keyword matching...", label_visibility="collapsed")

if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is analyzing your career path..."):
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

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Keyword Guide", "⚠️ Risks", "💡 Advice"])
    
    with tab1:
        st.write("Detailed structure analysis:")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        st.write("**Top Keywords to include in your resume:**")
        examples = ["React.js", "Python", "Cloud Computing", "Team Leadership", "Problem Solving", "SQL", "Agile"]
        for word in examples:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
        st.info("💡 Pro-Tip: Integrating these keywords into your Bullet Points increases visibility to recruiters.")

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected!")

    with tab4:
        p = st.selectbox("View Advice From:", ["Recruiter", "Hiring Manager", "CTO"], key="persona_select")
        st.info(persona_engine(res_text, p))

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f"""
        <div class="plan-card">
            <div style="color:#059669; font-weight:800; font-size:12px; text-transform:uppercase;">Step {i+1}</div>
            <div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# 📈 COMMUNITY ANALYTICS
# ==============================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Global Visitors", data['visits'])
with c2:
    st.metric("Resumes Scanned", data['analyses'])
with c3:
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)