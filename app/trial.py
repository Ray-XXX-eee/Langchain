import streamlit as st

st.session_state.trial_limit = st.secrets["TRIALS"]

def if_trial_available():
    print("trial print : " + str(st.session_state.trial_limit))
    if st.session_state.trial_limit > 0:
        return True
    else:
        return False

def trial_counter():
    while st.session_state.trial_limit > 0:
        st.session_state.trial_limit -= 1
        return st.session_state.trial_limit
    