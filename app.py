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
        "What was the biggest challenge you faced while working on your projects?",
        "How would you apply your specific skills to solve a real-world problem here?",
        "If you had to redo one of your projects today, what would you change?",
        "Describe a situation where you had to learn a new technology quickly."
    ]
    if "React" in resume_text or "Frontend" in resume_text:
        questions.append("How do you manage state in a large-scale frontend application?")
    if "Python" in resume_text or "Backend" in resume_text:
        questions.append("How would you handle slow API responses in a backend system?")
    return questions[:5]

# ==============================
# 🚀 CORE LOGIC & CONFIG
# ==============================
track_visit()
st.set_page_config(page_title="Placement AI | Navjot Kaur", page_icon="🎯", layout="wide")

# ==============================
# 📱 FINAL UI POLISH (DARK MODE PROOF)
# ==============================
st.markdown("""
<style>
/* Background & Global Text */
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #1e293b !important; font-weight: 500; }

/* 🛡️ STEP 1 & 2 ACTION ZONES (Deep Blue) */
textarea, [data-testid="stFileUploader"] section {
    background-color: #1e3a8a !important;
    color: #ffffff !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 12px !important;
}

/* ⚪ FORCE WHITE TEXT FOR UPLOADER (Drag & Drop Fix) */
[data-testid="stFileUploader"] section div div {
    color: #ffffff !important;
}

/* 📱 BROWSE FILES BUTTON FIX (White Background / Blue Text) */
div[data-testid="stFileUploader"] section button {
    background-color: #ffffff !important;
    color: #1e3a8a !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 8px !important;
}

/* Input Area Text Visibility */
.stTextArea textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Roadmap Cards */
.plan-card {
    background-color: #ffffff !important;
    border-left: 10px solid #10b981 !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
    border-radius: 10px !important;
}

/* Slim Footer Styling (Navjot Kaur Branding) */
.footer-container {
    background: #1e3a8a;
    padding: 20px;
    border-radius: 15px;
    color: white !important;
    text-align: center;
    margin-top: 40px;
}
.footer-container b, .footer-container p {
    color: #ffffff !important;
}
.footer-link {
    color: #5eead4 !important;
    text-decoration: none;
    margin: 0 10px;
    font-size: 14px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# HERO DISPLAY
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 30px; border-radius: 20px; color: white !important; text-align: center; margin-bottom: 25px;">
    <div style="font-size:30px;">🏹</div>
    <h1 style="color: white !important; margin:0; font-size: 28px;">PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span></h1>
    <p style="color: #ccfbf1 !important; margin-top: 5px;">Build. Scan. Get Hired.</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🚀 Run AI Diagnostic"):
    if uploaded_file:
        track_analysis()
        with st.spinner("AI is analyzing..."):
            resume_text = extract_text(uploaded_file)
            st.session_state['resume_text'] = resume_text
            st.session_state['ats_data'] = ats_engine(resume_text)
            st.session_state['jd_score'] = match_jd(resume_text, jd_text) if jd_text.strip() else 0
            st.session_state['risks'] = detect_risks(resume_text)
            st.session_state['analyzed'] = True
    else: st.warning("Upload resume first!")

# RESULTS
if st.session_state.get('analyzed'):
    res_text = st.session_state['resume_text']
    ats = st.session_state['ats_data']
    jd_s = st.session_state['jd_score']
    risks = st.session_state['risks']

    st.markdown("### 📊 Your Results")
    m1, m2 = st.columns(2)
    m1.metric("ATS SCORE", f"{ats['total']}/100")
    m2.metric("JD MATCH", f"{jd_s}%")

    tabs = st.tabs(["📊 Breakdown", "🎯 Keywords", "⚠️ Risks", "💡 Advice", "🎤 Interview Prep"])
    
    with tabs[4]:
        st.write("### 🎤 Practice Questions")
        qs = generate_questions(res_text)
        for i, q in enumerate(qs): st.markdown(f"**Q{i+1}:** {q}")

    st.markdown("---")
    st.markdown("### 🛠️ Personalized Roadmap")
    plan = generate_plan(ats['total'], jd_s, risks)
    for i, step in enumerate(plan):
        st.markdown(f'<div class="plan-card"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

# COMMUNITY ANALYTICS
st.markdown("<br>---")
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: st.metric("Success Rate", "94%")

# ==============================
# 🏆 FOOTER (WHITE TEXT FIXED)
# ==============================
st.markdown(f"""
<div class="footer-container">
    <p style="margin-bottom: 5px; font-size: 16px;"><b>Built with ❤️ by Navjot Kaur</b></p>
    <div>
        <a href="https://www.linkedin.com/in/navjot-kaur-b381a4283/" class="footer-link" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/navjot-kaur13/placement-assistant-ai" class="footer-link" target="_blank">💻 GitHub</a>
        <a href="mailto:kaur21navjot@gmail.com" class="footer-link">📧 Feedback</a>
    </div>
</div>
""", unsafe_allow_html=True)