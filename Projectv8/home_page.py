"""Define the hoem page"""

import streamlit as st

# from document_processor import get_keywords_from_data_folder
from app_utils import handle_user_input, initialize_model
from vector_store import load_local_vector_store

# from lda_utils import perform_lda


def home_page():
    """Home page to render"""
    st.title("RAG-Powered Document Query Chatbot")
    st.write("Ask questions about the content in the text files in the 'data' folder.")

    # Initialize vector store
    vector_store = load_local_vector_store()

    # Initialize model
    llm = initialize_model()

    # Inform the user about keyword-based queries
    st.write(
        """To query files, use "tell me about" or the name of the file in your prompt."""
    )

    # Handle user input and responses
    handle_user_input(llm, vector_store)
