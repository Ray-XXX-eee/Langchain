# app/inference.py
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


class Inference:
    def __init__(self,llm_name:str, temperature:float):
        self.llm_name = llm_name
        self.temperature = temperature
    
    def get_llm(self):
        """Returns the LLM model based on the selected parameters."""
        model = self.llm_name
        return ChatGroq(model=model)

    def build_prompt(self):
        """Creates a prompt template for querying the LLM."""
        return ChatPromptTemplate.from_template(
            """
            You are an expert knowledge assistant who can answer to the point about the
            <context>
            {context}
            <context>
            with proper point-wise explanation and complete examples if needed with 
            respect to the following user question:
            Question: {input}
            """
        )

    def answer_query(self, user_prompt: str):
        """Answers a query based on the retrieved document context."""
        if "vectors" not in st.session_state:
            st.error("Please process documents first!")
            return None  # Return None explicitly when no documents are available
        
        llm = self.get_llm()
        base_prompt = self.build_prompt()
        document_chain = create_stuff_documents_chain(llm, base_prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        response = retrieval_chain.invoke({"input": user_prompt})
        return response
