import streamlit as st
from app.inference import Inference
from app.trial import trial_counter

def display_chat():
    """Display chat history and enable auto-scrolling."""
    chat_container = st.empty()  # Holds chat messages dynamically

    with chat_container.container():
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(chat["user"])
            with st.chat_message("assistant"):
                st.markdown(chat["response"])

    # Auto-scroll effect
    st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown(
        """<script>
        var chatDiv = document.getElementById("scroll-to-bottom");
        chatDiv.scrollIntoView({ behavior: "smooth" });
        </script>""",
        unsafe_allow_html=True,
    )

def chat_interface(selected_model, temperature):
    """Handles user input, persists chat history, and triggers auto-scroll."""
    
    display_chat()  # Show previous messages

    user_prompt = st.chat_input("Type your message here...")

    if user_prompt:
        # Show user message instantly
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Get response from LLM
        inference_instance = Inference(llm_name=selected_model, temperature=temperature)
        response = inference_instance.answer_query(user_prompt=user_prompt)
        trial_counter()  # Deduct one trial if applicable

        # Show assistant response instantly
        with st.chat_message("assistant"):
            st.markdown(response['answer'])

        # Save to chat history
        st.session_state.chat_history.append({"user": user_prompt, "response": response['answer']})

        # Auto-scroll by forcing UI refresh
        # st.experimental_rerun()

    # Add "Clear Chat" button
    if st.session_state.chat_history != []:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
