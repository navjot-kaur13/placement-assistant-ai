import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

track_visit()
st.set_page_config(page_title="Placement Assistant AI", layout="wide")

# ==============================
# 🎨 Premium Startup UI Styling
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f8fafc, #e2e8f0); }
.block-container { padding-top: 4rem !important; }

/* Card Containers */
.stMetric, .stTabs, .stAlert {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    border: 1px solid #cbd5e1 !important;
}

/* Genuine Risk Items */
.risk-box {
    background-color: #fef2f2;
    color: #991b1b;
    padding: 15px;
    border-left: 6px solid #dc2626;
    border-radius: 8px;
    margin-bottom: 12px;
    font-weight: 500;
}

/* Genuine Improvement Plan Cards */
.plan-card {
    background-color: #ffffff;
    color: #1e293b;
    padding: 20px;
    border-top: 4px solid #10b981;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.step-label {
    color: #059669;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="background: #1e40af; padding: 40px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;">
    <h1 style="color: white !important; margin: 0;">🚀 Placement Assistant AI</h1>
    <p style="font-size:18px; opacity: 0.9;">Analyze. Improve. Get Placed.</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# ANALYZE LOGIC
# ==============================
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
with col2:
    jd_text = st.text_area("📌 Job Description", height=100, placeholder="Optional: Paste JD for better matching")

if st.button("🔍 Run Full AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("Our AI is scanning your profile..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else:
        st.warning("Please upload a resume first.")

if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    # DASHBOARD
    st.markdown("### 📈 Analysis Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS Score", f"{ats['total']}/100")
    m2.metric("JD Match", f"{jd_s}%")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Breakdown", "🎯 Matching", "⚠️ Critical Risks", "💡 Expert Advice"])

    with tab1:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])

    with tab3:
        if risks:
            st.markdown("#### 🚨 Issues that might get you rejected:")
            for r in risks:
                st.markdown(f'<div class="risk-box">✖ {r}</div>', unsafe_allow_html=True)
        else:
            st.success("Perfect! No structural risks detected.")

    with tab4:
        p = st.selectbox("Get feedback from:", ["Recruiter", "Hiring Manager", "CTO"], key="persona_fix")
        st.info(persona_engine(res_text, p))

    # GENUINE IMPROVEMENT PLAN (The Big Change)
    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap to Success")
    plan = generate_plan(ats['total'], jd_s, risks)
    
    plan_col1, plan_col2 = st.columns(2)
    for i, step in enumerate(plan):
        target_col = plan_col1 if i % 2 == 0 else plan_col2
        with target_col:
            st.markdown(f"""
            <div class="plan-card">
                <div class="step-label">Step {i+1}</div>
                <div style="font-weight: 500; margin-top: 5px;">{step}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================
# SIDEBAR ANALYTICS
# ==============================
data = load_data()
st.sidebar.markdown(f"**Community Impact:** {data['analyses']} Resumes Improved")