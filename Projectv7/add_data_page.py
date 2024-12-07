"""Page for loading in new data in different ways"""

import streamlit as st
from document_uploader import upload_and_vectorize
from app_utils import scrape_website


def data_page():
    """Add data page logic for rendering"""
    st.title("Use this page to add new data")

    st.divider()

    upload_and_vectorize()

    st.divider()

    scrape_website()
