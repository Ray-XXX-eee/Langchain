# app/main.py
import os
import streamlit as st
# from app.config import TRIAL_LIMIT
from app.document_processor import vector_embedding
from app.inference import Inference
from app.trial import *

import certifi

# trial_limit = None 
# st.session_state.trial_limit = trial_limit
init_trial_state()
os.environ["SSL_CERT_FILE"] = certifi.where()

st.set_page_config(page_title="KnowledgeBase RAG Agent :)", layout="wide")
st.title("KnowledgeBase RAG Agent :)")

# Sidebar: Model selection and pricing placeholder
with st.sidebar.expander("Choose Model:"):
    selected_model = st.selectbox("Select Model", ["gemma2-9b-it", "llama3-8b-8192"])
    temperature = st.slider("Temperature", min_value=0.0,max_value=1.0,step=0.1)
if if_trial_available():
    with st.sidebar.expander(f"Trial Left: {st.session_state.trial_limit}"):
        st.write(f"You have {st.session_state.trial_limit} Query trials left to try")
else:
    with st.sidebar.expander(f"No trial Left, enter your own API key below 👇",expanded=True):
        st.text_input("Enter your Groq API key here:")

st.sidebar.markdown("[Upgrade for more features](#)")  # Hyperlink to future pricing page

# Data folder
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Show available documents
existing_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
# st.subheader("Available Documents")
# if existing_files:
#     st.markdown("\n".join(f"- {file}" for file in existing_files))
# else:
#     st.write("No existing documents found in the 'data' folder.")

# Option: Use existing or upload your own
option = st.radio("Step 1 : Choose an option:", ("Use existing documents", "Upload your own"))

if option == "Upload your own":
    uploaded_files = st.file_uploader("Upload PDFs for processing", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(DATA_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("Uploaded files have been saved to the 'data' folder.")
elif option == "Use existing documents" and existing_files:
    selected_files = st.multiselect("Select available PDFs:", existing_files)
else:
    selected_files = None

# Processing button
if st.button("Start Processing"):
    file_to_process = None
    if option == "Upload your own" and uploaded_files:
        # Process first uploaded file for demo purposes
        file_to_process = os.path.join(DATA_DIR, uploaded_files[0].name)
    elif option == "Use existing documents" and selected_files:
        file_to_process = os.path.join(DATA_DIR, selected_files[0])
    
    if file_to_process:
        vector_embedding(file_to_process)
    else:
        st.error("Please select a document or upload one.")

# Show document details if available
with st.sidebar.expander("📄 Document Details"):
    if "metadata" in st.session_state:
        for file, pages in st.session_state.metadata.items():
            st.write(f"✅ `{os.path.basename(file)}` - **{pages} pages**")
        total_chunks = len(st.session_state.get("final_doc", []))
        total_tokens = sum(len(chunk.page_content) for chunk in st.session_state.get("final_doc", []))
        st.write(f"📌 **Total Chunks:** {total_chunks}")
        st.write(f"🔢 **Approximate Token Size:** {total_tokens} characters")

# Chat input
user_prompt = st.text_input("Ask anything about the selected documents!")
if user_prompt:
    inference = Inference(llm_name=selected_model,temperature=temperature)
    response = inference.answer_query(user_prompt=user_prompt)
    trial_counter()
   
    if response:
        st.write(response['answer'])
        with st.expander("Doc similarity search"):
            for doc in response.get('context', []):
                st.write(doc.page_content)
                st.write("---")
