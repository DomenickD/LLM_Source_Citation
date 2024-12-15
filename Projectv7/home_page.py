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

    # Load keywords from the data folder
    # keywords = get_keywords_from_data_folder(folder="./data")

    # Initialize UI components
    # TEMPERATURE, use_vector_store = initialize_ui()

    # Initialize model
    llm = initialize_model()

    # Inform the user about keyword-based queries
    st.write(
        """To query files, use "tell me about" or the name of the file in your prompt."""
    )

    # Handle user input and responses
    handle_user_input(llm, vector_store)

    # with st.expander("Current Topics in Documents"):
    #     # LDA Topics
    #     # st.subheader("Current Topics in Documents")
    #     lda_topics = perform_lda()
    #     for topic, keywords in lda_topics.items():
    #         st.write(f"**{topic}**: {', '.join([kw[0] for kw in keywords])}")
