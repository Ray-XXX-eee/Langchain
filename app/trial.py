# app/trial.py
import streamlit as st

def init_trial_state():
    # Initialize trial_limit in session_state if it doesn't exist yet.
    st.session_state.setdefault("trial_limit", int(st.secrets["TRIALS"]))

def if_trial_available():
    # print("Trial limit is: " + str(st.session_state.trial_limit))
    return st.session_state.trial_limit > 0

def trial_counter():
    if st.session_state.trial_limit > 0:
        st.session_state.trial_limit -= 1
