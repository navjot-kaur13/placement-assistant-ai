import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def ensure_initialized():
    """AI Safety Check: Google Sheets se data load karke session state set karta hai"""
    if "visitors" not in st.session_state or "analyses" not in st.session_state:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(worksheet="Sheet1")
            # Cleaning column names for safety
            df.columns = df.columns.str.strip()
            
            st.session_state.visitors = int(df.loc[df['metric_name'] == 'visitors', 'value'].values[0])
            st.session_state.analyses = int(df.loc[df['metric_name'] == 'scans', 'value'].values[0])
        except:
            # Fallback agar connection fail ho (Aapke base numbers)
            st.session_state.visitors = 406
            st.session_state.analyses = 52

def load_data():
    ensure_initialized()
    return {
        "visits": st.session_state.visitors, 
        "analyses": st.session_state.analyses
    }

def track_visit():
    ensure_initialized()
    if 'has_visited' not in st.session_state:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(worksheet="Sheet1")
            df.columns = df.columns.str.strip()
            
            # Increment in session and sheet
            st.session_state.visitors += 1
            df.loc[df['metric_name'] == 'visitors', 'value'] = st.session_state.visitors
            
            conn.update(worksheet="Sheet1", data=df)
            st.session_state.has_visited = True
        except:
            st.session_state.visitors += 1 # Local update if sheet fails

def track_analysis():
    ensure_initialized()
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1")
        df.columns = df.columns.str.strip()
        
        # Increment in session and sheet
        st.session_state.analyses += 1
        df.loc[df['metric_name'] == 'scans', 'value'] = st.session_state.analyses
        
        conn.update(worksheet="Sheet1", data=df)
    except:
        st.session_state.analyses += 1 # Local update if sheet fails

def get_current_stats():
    # Same as load_data to maintain compatibility with your app.py
    return load_data()