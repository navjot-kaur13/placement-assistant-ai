import streamlit as st

def ensure_initialized():
    """AI Safety Check: Variables ko setup karta hai agar wo missing hon"""
    if "visitors" not in st.session_state:
        st.session_state.visitors = 405  # Aapka last known high score
    if "analyses" not in st.session_state:
        st.session_state.analyses = 52

def load_data():
    ensure_initialized()
    return {
        "visits": st.session_state.visitors, 
        "analyses": st.session_state.analyses
    }

def track_visit():
    ensure_initialized()
    # Ek browser session mein sirf ek baar count badhega
    if 'has_visited' not in st.session_state:
        st.session_state.visitors += 1
        st.session_state.has_visited = True

def track_analysis():
    ensure_initialized()
    st.session_state.analyses += 1

def get_current_stats():
    ensure_initialized()
    return {
        "visits": st.session_state.visitors,
        "analyses": st.session_state.analyses
    }