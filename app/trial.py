import streamlit as st

if "trial_limit" not in st.session_state:
    st.session_state.setdefault("trial_limit", int(st.secrets["TRIALS"]))

def if_trial_available():
    print ("test limit print : "+ str(st.session_state.trial_limit))
    return st.session_state.trial_limit > 0

def trial_counter():
    if st.session_state.trial_limit > 0:
        st.session_state.trial_limit -= 1
    