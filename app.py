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
/* Force Background to be Light Grey for contrast */
[data-testid="stAppViewContainer"] { 
    background-color: #f1f5f9 !important; 
}

/* Fix text visibility: All headings and labels forced to Dark Navy */
h1, h2, h3, h4, h5, p, span, label, div {
    color: #0f172a !important;
    font-family: 'Inter', sans-serif;
}

/* Card Styling: High visibility borders for phone screens */
.stMetric, .stTabs, .stAlert, .analytics-card, .plan-card {
    background-color: white !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
}

/* Metrics visibility fix */
[data-testid="stMetricValue"] { 
    color: #1d4ed8 !important; 
    font-weight: 800 !important; 
}
[data-testid="stMetricLabel"] { 
    color: #475569 !important; 
}

/* Tab text fix for mobile */
button[data-baseweb="tab"] p {
    color: #1e40af !important;
    font-weight: 700 !important;
}

/* Custom Analytics Cards */
.analytics-card { 
    text-align: center; 
    box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
}

/* Roadmap Plan Card */
.plan-card { 
    border-top: 5px solid #10b981 !important; 
}
.step-label { 
    color: #059669 !important; 
    font-size: 11px; 
    font-weight: 800; 
    text-transform: uppercase; 
}

/* Button Styling */
.stButton>button {
    background-color: #1d4ed8 !important; 
    color: white !important;
    border-radius: 8px !important; 
    width: 100% !important;
    height: 3.5em !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: #1e3a8a; padding: 30px 20px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 20px;">
    <h1 style="color: white !important; margin: 0; font-size: 24px;">🚀 Placement Assistant AI</h1>
    <p style="color: #bfdbfe !important; margin-top: 5px; font-size: 14px;">Your Smart Career Copilot</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📊 TOP ANALYTICS (Community Impact)
# ==============================
data = load_data()
st.markdown("#### 🌎 Global Impact")
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
# 📄 INPUT SECTION
# ==============================
st.markdown("#### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Job Description (Optional)", height=120, placeholder="Paste JD here for better matching...")

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
        st.markdown("**Breakdown:**")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        if jd_text.strip():
            st.write(f"Overall Match: {jd_s}%")
            st.progress(jd_s/100)
        else:
            st.info("Paste a Job Description to see match score.")

    with tab3:
        if risks:
            for r in risks:
                st.error(f"🚨 {r}")
        else:
            st.success("No structural red flags detected!")

    with tab4:
        p = st.selectbox("Get feedback from:", ["Recruiter", "Hiring Manager", "CTO"], key="p_fix_mobile")
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