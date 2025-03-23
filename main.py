import os
import streamlit as st
import certifi

from app.trial import init_trial_state, if_trial_available
from app.ui.sidebar import SidebarUI
from app.ui.main_ui import MainUI

os.environ["SSL_CERT_FILE"] = certifi.where()

# Initialize session state for trials
init_trial_state()

# Ensure chat history is initialized in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="KnowledgeBase RAG Agent :)", layout="wide")
st.title("KnowledgeBase RAG Agent :)")

# Create UI objects
sidebar_ui = SidebarUI()
sidebar_ui.choose_model()
sidebar_ui.display_trial_info(if_trial_available, st.session_state.trial_limit)


main_ui = MainUI(sidebar_ui)
option = main_ui.display_options()
st.session_state["option"] = option
main_ui.process_documents()

# Display chat interface
main_ui.display_chat_comp()

# Display document details in sidebar
sidebar_ui.display_doc_details()
sidebar_ui.display_upgrade_link()
