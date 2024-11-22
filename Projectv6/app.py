"""
Streamlit Application for Interactive LLM and Vector Store Queries.
"""

import streamlit as st
from document_processor import get_keywords_from_data_folder, get_context_for_question
from app_utils import initialize_ui, handle_user_input, initialize_model
from vector_store import initialize_chroma_vector_store
from utils import scrape_webpage

# Initialize vector store
vector_store = initialize_chroma_vector_store()

# Load keywords from the data folder
keywords = get_keywords_from_data_folder(data_folder="./data")

# Initialize UI components
TEMPERATURE, scrape_message = initialize_ui()

# Initialize model
llm = initialize_model(temperature=TEMPERATURE)

# Inform the user about keyword-based queries
st.write(
    """To query files, use "tell me about" or the name of the file in your prompt."""
)

# Handle user input and responses
handle_user_input(llm, vector_store, keywords)
