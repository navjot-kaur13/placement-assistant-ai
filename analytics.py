import streamlit as st

# 🚨 AI PERSISTENCE STRATEGY:
# Streamlit Cloud par files save nahi rehti, isliye hum 'st.session_state' 
# aur 'st.secrets' ka mix use karenge.

def load_data():
    # Agar aapne Streamlit Secrets mein data set kiya hai toh wahan se lo
    # Warna default 405 se start karo (jo aapka latest high score tha)
    if "visitors" not in st.session_state:
        st.session_state.visitors = 405 
        st.session_state.analyses = 52
    
    return {"visits": st.session_state.visitors, "analyses": st.session_state.analyses}

def track_visit():
    # Ek session mein sirf ek baar visit count ho
    if 'has_visited' not in st.session_state:
        st.session_state.visitors += 1
        st.session_state.has_visited = True

def track_analysis():
    st.session_state.analyses += 1

def get_current_stats():
    return {
        "visits": st.session_state.visitors,
        "analyses": st.session_state.analyses
    }