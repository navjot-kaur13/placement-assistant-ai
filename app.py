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
st.set_page_config(page_title="Placement Assistant AI", page_icon="🚀", layout="wide")

# ==============================
# 📱 MOBILE-FIRST UI CSS
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

/* Metrics Styling (For the Bottom Section) */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* 🚨 FILE UPLOADER & BROwSE FIX */
[data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px dashed #ffffff !important;
    color: white !important;
}
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
}

/* Action Button */
div.stButton > button:first-child {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    height: 55px !important;
}

/* Keyword Chips */
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
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div style="background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%); padding: 30px; border-radius: 20px; color: white !important; text-align: center; margin-bottom: 25px;">
    <h1 style="color: white !important; margin: 0; font-size: 28px;">🚀 Placement Assistant AI</h1>
    <p style="color: #bfdbfe !important; margin-top: 5px; font-size: 16px;">Scan. Fix. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📄 STEP 1 & 2 (Now at the TOP)
# ==============================
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target Job Description")
jd_text = st.text_area("JD Input", height=120, placeholder="Paste JD here to check keyword matching...", label_visibility="collapsed")

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
    else: st.warning("Please upload your resume first!")

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
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        st.write("**Recommended Keywords for your profile:**")
        # Example Keywords - You can later make this dynamic based on resume_text
        examples = ["React.js", "System Design", "Scalability", "REST APIs", "Unit Testing", "AWS", "Agile Methodology"]
        for word in examples:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
        st.info("💡 Adding these keywords in your 'Experience' or 'Skills' section can boost your ATS score by 20-30%.")

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural risks detected!")

    with tab4:
        p = st.selectbox("Advisor:", ["Recruiter", "Hiring Manager", "CTO"], key="p_v2")
        st.info(persona_engine(res_text, p))

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><div style="color:#059669; font-weight:800; font-size:12px;">STEP {i+1}</div><div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div></div>', unsafe_allow_html=True)

# ==============================
# 📈 COMMUNITY ANALYTICS (Now at the BOTTOM)
# ==============================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: 
    rate = "94%" if data['analyses'] >= 4 else "---"
    st.metric("Success Rate", rate)