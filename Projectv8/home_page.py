"""Define the home page"""

import streamlit as st
from app_utils import handle_user_input, initialize_model
from vector_store import load_local_vector_store


def home_page():
    """Home page to render"""
    st.title("RAG-Powered Document Query Chatbot")
    st.caption("Powered by the Ollama Language Model (v3.2)")

    # Initialize vector store
    vector_store = load_local_vector_store()

    # Initialize model
    llm = initialize_model()

    # Inform the user about keyword-based queries
    st.write(
        """To query files, use "tell me about" somewhere in the prompt.\
            This tells the LLM that you want to use RAG and not just chat."""
    )

    # Handle user input and responses
    handle_user_input(llm, vector_store)
