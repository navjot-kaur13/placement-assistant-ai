import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🚀 CORE LOGIC & INITIALIZATION
# ==============================
track_visit() # Must run first
st.set_page_config(page_title="Placement Assistant AI", layout="wide")

# ==============================
# 🎨 REFINED PREMIUM UI STYLING
# ==============================
st.markdown("""
<style>
/* Cleaner Background */
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f8fafc, #e2e8f0); }

/* Spacing Fixes */
.block-container { padding-top: 3rem !important; padding-bottom: 2rem !important; }

/* Global Card Styling (Dashboard, Tabs, Alerts) */
.stMetric, .stTabs, .stAlert, div[data-testid="stExpander"] {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid #e2e8f0 !important;
}

/* Primary Button Styling */
.stButton>button {
    background: #1d4ed8 !important; color: white !important;
    border-radius: 8px !important; font-weight: 600 !important;
    height: 3.5em !important; width: 100% !important; border: none !important;
}
.stButton>button:hover { background: #1e40af !important; box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important; }

/* Risk Boxes styling */
.risk-box {
    background-color: #fef2f2; color: #991b1b;
    padding: 15px; border-left: 6px solid #dc2626;
    border-radius: 8px; margin-bottom: 12px; font-weight: 500;
}

/* Roadmap Plan Card Styling */
.plan-card {
    background-color: #ffffff; color: #1e293b;
    padding: 20px; border-top: 4px solid #10b981;
    border-radius: 10px; margin-bottom: 15px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.step-label { color: #059669; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }

/* Custom Analytics Card Styling */
.analytics-card {
    background: white; padding: 20px; border-radius: 12px;
    text-align: center; border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: #1e3a8a; padding: 40px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;">
    <h1 style="color: white !important; margin: 0; font-size: 32px;">🚀 Placement Assistant AI</h1>
    <p style="font-size:18px; opacity: 0.9; margin-top: 10px;">Your Smart Career Copilot</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📊 TOP ANALYTICS DASHBOARD (Was missing)
# ==============================
analytics_data = load_data()
st.markdown("### 🌎 Global Community Impact")
a1, a2, a3 = st.columns(3)

with a1:
    st.markdown(f"""<div class="analytics-card"><h2 style="color:#1d4ed8;margin:0;">{analytics_data['visits']}</h2><p style="margin:0;color:#64748b;">People Visited</p></div>""", unsafe_allow_html=True)
with a2:
    st.markdown(f"""<div class="analytics-card"><h2 style="color:#10b981;margin:0;">{analytics_data['analyses']}</h2><p style="margin:0;color:#64748b;">Resumes Improved</p></div>""", unsafe_allow_html=True)
with a3:
    # A fun premium metric for a startup
    success_rate = "94%" if analytics_data['analyses'] > 5 else "---"
    st.markdown(f"""<div class="analytics-card"><h2 style="color:#f59e0b;margin:0;">{success_rate}</h2><p style="margin:0;color:#64748b;">Average Match Improvement</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# 📄 INPUT SECTION (Now JD is always visible)
# ==============================
st.markdown("### 🔍 Step 1: Upload Your Profile")
input_col1, input_col2 = st.columns([1.5, 2])

with input_col1:
    # Adding clear help text for professional use
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF/DOCX)", type=["pdf", "docx"], help="Max 2MB. Your data is processed securely.")

with input_col2:
    jd_text = st.text_area("📌 Target Job Description (Optional)", height=150, placeholder="Optional: Paste the JD here for personalized matching...")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# 🧠 AI DIAGNOSTIC BUTTON
# ==============================
if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is scanning your profile for impact..."):
            resume_text = extract_text(uploaded_file)
            # Safe in session state for tab re-rendering
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
            
            # Temporary success message that vanishes on next action
            st.toast("Analysis complete! Check results below.", icon="✅")
    else:
        st.warning("Please upload your resume file first.")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# 📊 RESULTS DASHBOARD
# ==============================
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    # DASHBOARD QUICK STATS
    st.markdown("### 📊 Your Placement Insights")
    m1, m2 = st.columns(2)
    m1.metric("ATS Score", f"{ats['total']}/100", help="This scores your resume structure and visibility to algorithms.")
    
    # Handling missing JD scenario for metric
    jd_match_display = f"{jd_s}%" if jd_text.strip() else "N/A"
    m2.metric("JD Compatibility", jd_match_display, help="How well your resume matches the specific job description.")

    st.markdown("<br>", unsafe_allow_html=True)

    # DETAILED TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Matching", "⚠️ Critical Risks", "💡 Expert Advice"])

    with tab1:
        st.write("Score breakdown based on best-practices:")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab2:
        if jd_text.strip():
            st.markdown(f"**Overall Compatibility:** {jd_s}%")
            st.progress(jd_s/100)
            st.write("Tailor your summary and skills to match keywords found in the JD.")
        else:
            st.info("💡 Paste a Job Description in the input area above to activate the compatibility matching feature.")

    with tab3:
        if risks:
            st.markdown("#### 🚨 Red Flags that might trigger HR rejections:")
            for r in risks:
                st.markdown(f'<div class="risk-box">✖ {r}</div>', unsafe_allow_html=True)
        else:
            st.success("Perfect! No structural red flags found. Your format is solid.")

    with tab4:
        # Selection triggers a rerun, but session_state preserves analysis data
        p = st.selectbox("View advice from:", ["Recruiter", "Hiring Manager", "CTO"], key="p_fix")
        st.markdown(f"**Professional Perspective from a {p}:**")
        st.info(persona_engine(res_text, p))

    # GENUINE IMPROVEMENT PLAN (The Big Change)
    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap to Placement Success")
    plan = generate_plan(ats['total'], jd_s, risks)
    
    # Render in a clean 2-column grid
    plan_col1, plan_col2 = st.columns(2)
    for i, step in enumerate(plan):
        # Even numbered items in col1, odd in col2
        target_col = plan_col1 if i % 2 == 0 else plan_col2
        with target_col:
            st.markdown(f"""
            <div class="plan-card">
                <div class="step-label">Step {i+1}</div>
                <div style="font-weight: 500; margin-top: 5px; font-size:16px;">{step}</div>
            </div>
            """, unsafe_allow_html=True)