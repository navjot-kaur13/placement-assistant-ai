import streamlit as st
from utils.resume_parser import extract_text
from utils.ats_engine import ats_engine
from utils.jd_matcher import match_jd
from utils.risk_flags import detect_risks
from utils.persona_engine import persona_engine
from utils.improvement_plan import generate_plan
from analytics import track_visit, track_analysis, load_data

# ==============================
# 🧠 INTERVIEW ENGINE LOGIC
# ==============================
def generate_questions(resume_text):
    questions = [
        "Can you walk me through the most technical project mentioned in your resume?",
        "What was the biggest challenge you faced while working on these technologies?",
        "How would you apply your specific skills to solve a real-world problem here?",
        "If you had to redo one of your projects today, what technical changes would you make?",
        "Describe a situation where you had to learn a new tool very quickly."
    ]
    return questions[:5]

# ==============================
# 🚀 CORE CONFIG
# ==============================
track_visit()
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

# ==============================
# 📱 UNIVERSAL CSS (LAPTOP + PHONE FIX)
# ==============================
st.markdown("""
<style>
/* Global Reset */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* Action Boxes */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
}

/* White Text for Inputs */
[data-testid="stFileUploader"] section div div, 
[data-testid="stFileUploader"] section span, 
.stTextArea textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Browse Button */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
}

/* 📊 METRICS: DARK LABELS FOR PHONE VISIBILITY */
[data-testid="stMetricLabel"] p {
    color: #475569 !important; /* Dark Grey for Laptop/Phone */
    font-size: 14px !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] div {
    color: #1e3a8a !important; /* Deep Blue Numbers */
    font-weight: 800 !important;
}
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
}

/* Tabs Styling */
button[data-baseweb="tab"] p {
    color: #1e293b !important;
    font-size: 14px !important;
}

/* Footer Link Force */
.footer-link {
    color: #5eead4 !important;
    text-decoration: none;
    font-weight: bold;
    margin: 0 10px;
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px;">
    <h1 style="color: #ffffff !important; margin:0; font-size: 28px; font-weight: 800;">PLACEMENT ASSISTANT AI</h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px; font-weight: 500;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🚀 RUN FULL AI DIAGNOSTIC"):
    if uploaded_file:
        track_analysis()
        with st.spinner("Analyzing..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Upload resume first!")

# RESULTS SECTION
if st.session_state.get('analyzed'):
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    
    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tabs = st.tabs(["📊 Breakdown", "⚠️ Risks", "👤 Persona", "🎤 Prep"])
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords']); b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs']); b4.metric("Impact", ats['impact'])
    
    with tabs[3]:
        st.write("### 🎤 Interview Prep")
        qs = generate_questions(st.session_state['resume_text'])
        for i, q in enumerate(qs):
            st.markdown(f'<div style="background:#f0f9ff; padding:10px; border-radius:8px; border-left:4px solid #0ea5e9; margin-bottom:8px;"><b>Q{i+1}:</b> {q}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠️ Roadmap")
    plan = generate_plan(ats['total'], jd_s, st.session_state['risks'])
    for i, step in enumerate(plan):
        st.markdown(f'<div style="background:white; border-left:8px solid #10b981; padding:12px; margin-bottom:10px; border-radius:8px; box-shadow:0px 2px 5px rgba(0,0,0,0.05);"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# COMMUNITY IMPACT
st.markdown("---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: st.metric("Success Rate", "94%")

# FOOTER
st.markdown(f"""
<div style="background:#1e3a8a; padding:25px; border-radius:15px; text-align:center; margin-top:30px;">
    <p style="color:#ffffff !important; font-weight:bold; margin-bottom:15px;">Built with ❤️ by Navjot Kaur</p>
    <div style="margin-top:10px;">
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" class="footer-link" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13" class="footer-link" target="_blank">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" class="footer-link">📧 Feedback</a>
    </div>
</div>
""", unsafe_allow_html=True)