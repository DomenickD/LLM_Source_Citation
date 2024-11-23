"""
Streamlit Application for Interactive LLM and Vector Store Queries.

This module implements a Streamlit-based user interface for interacting \
    with a local LLM (Large Language Model) and a vector store. \
        It initializes the required components, processes user input, \
            and provides responses based on data from a specified folder.

Modules:
- document_processor: Handles keyword extraction \
    and context retrieval from the data folder.
- app_utils: Provides utilities for UI initialization, \
    user input handling, and LLM setup.
- vector_store: Manages the loading and querying of a local vector store.

Usage:
Run this script to launch the Streamlit app. The user can input queries to \
    interact with the model and retrieve information.
"""

import streamlit as st
from document_processor import get_keywords_from_data_folder
from app_utils import initialize_ui, handle_user_input, initialize_model
from vector_store import load_local_vector_store


# Initialize vector store
vector_store = load_local_vector_store()

# Load keywords from the data folder
keywords = get_keywords_from_data_folder(data_folder="./data")

# Initialize UI components
# TEMPERATURE, use_vector_store = initialize_ui()
temperature = initialize_ui()

# Initialize model
llm = initialize_model(temperature=temperature)

# Inform the user about keyword-based queries
st.write(
    """To query files, use "tell me about" or the name of the file in your prompt."""
)


# Handle user input and responses
handle_user_input(llm, vector_store, keywords)
