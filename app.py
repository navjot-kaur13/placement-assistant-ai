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
st.set_page_config(page_title="Placement AI | Career Copilot", page_icon="🎯", layout="wide")

# ==============================
# 📱 UI CSS (FIXED SPACING)
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: #000000 !important; font-weight: 500; }

/* Fixed Roadmap Card Visibility */
.plan-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 10px solid #10b981 !important;
    padding: 20px !important;
    margin-top: 10px !important;
    margin-bottom: 15px !important;
    border-radius: 12px !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
    display: block !important; /* Forces visibility */
}

.hero-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); 
    padding: 30px 20px; 
    border-radius: 25px; 
    color: white !important; 
    text-align: center; 
    margin-bottom: 30px; 
}
.hero-title { font-size: 32px; font-weight: 800; color: white !important; margin:0; }
.hero-subtitle { font-size: 15px; color: #ccfbf1 !important; margin-top: 5px; }

@media (max-width: 640px) {
    .hero-title { font-size: 22px; }
    .hero-container { padding: 20px 10px; }
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown(f"""
<div class="hero-container">
    <div style="font-size:30px;">🏹</div>
    <h1 class="hero-title">PLACEMENT ASSISTANT <span style="color: #5eead4;">AI</span></h1>
    <p class="hero-subtitle">"Precision in every scan. Accuracy in every roadmap."</p>
</div>
""", unsafe_allow_html=True)

# INPUTS
st.markdown("### 🔍 Step 1: Upload Your Profile")
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("### 📌 Step 2: Target JD")
jd_text = st.text_area("JD", height=120, placeholder="Paste JD here...", label_visibility="collapsed")

if st.button("🔍 Run Full AI Diagnostic"):
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
    
    with tabs[0]:
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Keywords", ats['keywords'])
        b2.metric("Structure", ats['sections'])
        b3.metric("Verbs", ats['verbs'])
        b4.metric("Impact", ats['impact'])
    with tabs[1]:
        for word in ["React.js", "Python", "Cloud", "Leadership", "SQL", "Agile"]:
            st.markdown(f'<span class="keyword-chip">{word}</span>', unsafe_allow_html=True)
    with tabs[2]:
        if risks:
            for r in risks: st.error(f"🚨 {r}")
        else: st.success("Safe!")
    with tabs[3]:
        p = st.selectbox("Advisor:", ["Recruiter", "Hiring Manager", "CTO"], key="adv")
        st.info(persona_engine(res_text, p))
    with tabs[4]:
        qs = generate_questions(res_text)
        for i, q in enumerate(qs): st.write(f"**Q{i+1}:** {q}")

    # 🛠️ THE ROADMAP (FORCE RE-RENDER)
    st.markdown("<br>---", unsafe_allow_html=True)
    st.markdown("### 🛠️ Personalized Roadmap to Success")
    plan = generate_plan(ats['total'], jd_s, risks)
    
    # Using a container to ensure it renders above analytics
    roadmap_container = st.container()
    with roadmap_container:
        for i, step in enumerate(plan):
            st.markdown(f"""
            <div class="plan-card">
                <div style="color:#059669; font-weight:800; font-size:12px; text-transform:uppercase;">Step {i+1}</div>
                <div style="font-weight:700; margin-top:5px; font-size:16px;">{step}</div>
            </div>
            """, unsafe_allow_html=True)

# COMMUNITY ANALYTICS (Move down with more padding)
st.markdown("<br><br><br><br>---", unsafe_allow_html=True)
st.markdown("### 🌍 Community Impact")
data = load_data()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Global Visitors", data['visits'])
with c2: st.metric("Resumes Scanned", data['analyses'])
with c3: st.metric("Success Rate", "94%")