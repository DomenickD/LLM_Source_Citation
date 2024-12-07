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
from app_utils import handle_user_input, initialize_model
from vector_store import load_local_vector_store
from streamlit_option_menu import option_menu

# Load vector store
try:
    vector_store = load_local_vector_store()
except Exception as e:
    vector_store = None
    st.error(f"Failed to load vector store: {e}")

# Initialize model
llm = initialize_model()

# Multi-page navigation
page = option_menu(
    "Main Menu",
    ["Query Assistant", "Upload & Web Scraper"],
    icons=["chat", "cloud-upload"],
    menu_icon="menu",
    default_index=0,
    orientation="horizontal",
)

if page == "Query Assistant":
    if vector_store:
        st.write(
            """To query files, use "tell me about" or the name of the file in your prompt."""
        )
        handle_user_input(llm, vector_store)
    else:
        st.error("Please upload and train documents before querying.")

elif page == "Upload & Web Scraper":
    from upload_and_scraper_page import render_upload_and_scraper_page

    # Render the upload and scraper page
    render_upload_and_scraper_page()
