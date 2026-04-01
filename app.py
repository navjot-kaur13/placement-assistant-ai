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
# 📱 MOBILE-OPTIMIZED HIGH CONTRAST UI
# ==============================
st.markdown("""
<style>
/* Background Contrast */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* Global Text Visibility */
h1, h2, h3, h4, h5, p, span, label { color: #1e293b !important; }

/* FIX: File Uploader Box & Text */
[data-testid="stFileUploader"] section {
    background-color: #2563eb !important; /* Blue background */
    border: 2px dashed #ffffff !important;
    border-radius: 10px !important;
    padding: 20px !important;
}

/* Force File Uploader Text to White */
[data-testid="stFileUploader"] section div div { color: white !important; }
[data-testid="stFileUploader"] small { color: #e0e7ff !important; font-weight: bold !important; }

/* Browse Files Button Inside Uploader */
[data-testid="stFileUploader"] button {
    background-color: white !important;
    color: #1d4ed8 !important;
    border-radius: 5px !important;
}

/* Card Styling */
.stMetric, .stTabs, .stAlert, .analytics-card, .plan-card {
    background-color: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}

/* Tab Active Color */
button[data-baseweb="tab"] p { color: #1d4ed8 !important; font-weight: 700 !important; }

/* Roadmap Step Labels */
.step-label { color: #059669 !important; font-size: 11px; font-weight: 800; text-transform: uppercase; }

/* Main Analyze Button */
.stButton>button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important; border-radius: 8px !important;
    font-weight: bold !important; height: 3.5em !important; border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: #1e3a8a; padding: 30px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 20px;">
    <h1 style="color: white !important; margin: 0; font-size: 24px;">🚀 Placement Assistant AI</h1>
    <p style="color: #bfdbfe !important; margin-top: 5px; font-size: 14px;">Analyze. Improve. Get Placed.</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📊 TOP ANALYTICS
# ==============================
data = load_data()
a1, a2, a3 = st.columns(3)
with a1:
    st.markdown(f'<div class="analytics-card"><h3 style="margin:0; color:#1d4ed8 !important;">{data["visits"]}</h3><p style="margin:0; font-size:12px;">Visits</p></div>', unsafe_allow_html=True)
with a2:
    st.markdown(f'<div class="analytics-card"><h3 style="margin:0; color:#10b981 !important;">{data["analyses"]}</h3><p style="margin:0; font-size:12px;">Analyzed</p></div>', unsafe_allow_html=True)
with a3:
    rate = "94%" if data['analyses'] > 5 else "---"
    st.markdown(f'<div class="analytics-card"><h3 style="margin:0; color:#f59e0b !important;">{rate}</h3><p style="margin:0; font-size:12px;">Success</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# 📄 INPUT SECTION (FIXED VISIBILITY)
# ==============================
st.markdown("#### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Select your Resume", type=["pdf", "docx"])

st.markdown("#### 📌 Step 2: Target Job Description")
jd_text = st.text_area("JD Area", height=100, placeholder="Paste Job Description here...", label_visibility="collapsed")

# ==============================
# 🧠 AI DIAGNOSTIC BUTTON
# ==============================
if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is scanning your profile..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else:
        st.warning("Please upload a resume first.")

# ==============================
# 📊 RESULTS DISPLAY
# ==============================
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("#### 📊 Your Insights")
    m1, m2 = st.columns(2)
    m1.metric("ATS Score", f"{ats['total']}/100")
    m2.metric("JD Match", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Match", "⚠️ Risks", "💡 Advice"])

    with tab1:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        if jd_text.strip():
            st.progress(jd_s/100)
        else:
            st.info("Paste a Job Description to see match score.")

    with tab3:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("No structural red flags detected!")

    with tab4:
        p = st.selectbox("Perspective:", ["Recruiter", "Hiring Manager", "CTO"], key="p_fix_final")
        st.info(persona_engine(res_text, p))

    # ROADMAP PLAN
    st.markdown("---")
    st.markdown("#### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f"""
        <div class="plan-card">
            <div class="step-label">Step {i+1}</div>
            <div style="font-weight: 700; margin-top: 5px; color: #1e293b;">{step}</div>
        </div>
        """, unsafe_allow_html=True)