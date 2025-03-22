# app/document_processor.py
import os
import time
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import TRIAL_LIMIT

def vector_embedding(file):
    # Trial usage: Limit to TRIAL_LIMIT documents per session
    trial_counter = st.session_state.get("trial_counter", 0)
    if trial_counter >= TRIAL_LIMIT:
        st.error("Trial limit reached. Please upgrade for more documents.")
        return None

    st.write("📥 **Loading PDFs...**")
    start_time = time.time()

    loader = PyPDFLoader(file)
    docs = loader.load()

    # Update trial counter based on the number of documents processed
    st.session_state.trial_counter = trial_counter + 1

    # Get metadata (e.g., number of pages)
    num_pages = {doc.metadata['source']: doc.metadata.get('page', 0) + 1 for doc in docs}
    st.session_state.metadata = num_pages

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_doc = text_splitter.split_documents(docs)

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = FAISS.from_documents(final_doc, embeddings)

    # Store in session state
    st.session_state.vectors = vectors
    st.session_state.final_doc = final_doc

    elapsed_time = time.time() - start_time
    st.success(f"✅ **Vectorstore DB is ready!** (Processed in {elapsed_time:.2f} seconds)")
    return vectors
