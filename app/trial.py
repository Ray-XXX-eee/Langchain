from app.config import TRIAL_LIMIT
import streamlit as st

st.session_state.trial_limit = TRIAL_LIMIT 

def if_trial_available():
    if st.session_state.trial_limit > 0:
        return True
    else:
        return False

def trial_counter():
    while st.session_state.trial_limit > 0:
        st.session_state.trial_limit -= 1
        return st.session_state.trial_limit
    