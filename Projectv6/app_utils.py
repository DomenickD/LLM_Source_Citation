"""
Utility Functions for Handling User Input and UI Interaction.
"""

import streamlit as st
from document_processor import get_context_for_question


def handle_user_input(llm, vector_store):
    """
    Handle user input and generate responses based on queries.
    """
    if "message_history" not in st.session_state:
        st.session_state.message_history = []

    for msg in st.session_state.message_history:
        if isinstance(msg, str):
            st.write(f"**Bot:** {msg}")

    with st.form(key="input_form", clear_on_submit=True):
        user_question = st.text_input("Ask a question:")
        submit_button = st.form_submit_button("Submit")

    if submit_button and user_question:
        context, source_info = get_context_for_question(vector_store, user_question)

        # Display the context and source information
        st.write("### Context")
        st.write(context)
        st.write(f"**Sources:** {source_info}")

        # Generate response
        response = llm.generate_response(context, user_question)
        st.session_state.message_history.append(f"Bot: {response}")
        st.write(f"**Bot:** {response}")
