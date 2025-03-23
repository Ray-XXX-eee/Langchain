import os
import streamlit as st
from app.document_processor import vector_embedding
from app.ui.chat import chat_interface  # Import chat module

class MainUI:
    def __init__(self, sidebar_ui):
        self.sidebar = sidebar_ui
        self.uploaded_files = None
        self.selected_files = None

    def display_options(self):
        """Display radio button for document option and file uploader or selector."""
        option = st.radio("***Step 1: Choose an option:***", ("Use existing documents", "Upload your own"))
        DATA_DIR = "data"
        os.makedirs(DATA_DIR, exist_ok=True)

        if option == "Upload your own":
            self.uploaded_files = st.file_uploader("Upload PDFs for processing", type=["pdf"], accept_multiple_files=True)
            if self.uploaded_files:
                for uploaded_file in self.uploaded_files:
                    file_path = os.path.join(DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                st.success("Uploaded files have been saved to the 'data' folder.")
        elif option == "Use existing documents":
            existing_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
            if existing_files:
                self.selected_files = st.multiselect("**Select available PDFs:**", existing_files)
            else:
                st.warning("No existing documents found in the 'data' folder.")
        
        return option

    def process_documents(self):
        """Process the document selected or uploaded."""
        DATA_DIR = "data"
        file_to_process = None
        option = st.session_state.get("option", "Use existing documents")

        if option == "Upload your own" and self.uploaded_files:
            file_to_process = os.path.join(DATA_DIR, self.uploaded_files[0].name)
        elif option == "Use existing documents" and self.selected_files:
            file_to_process = os.path.join(DATA_DIR, self.selected_files[0])

        if st.button("Process PDF"):
            if file_to_process:
                vector_embedding(file_to_process)
            else:
                st.error("Please select a document or upload one.")

    def display_chat(self, selected_model, temperature):
        """Call chat interface from chat.py."""
        chat_interface(selected_model, temperature)  # Calls the modular chat function
