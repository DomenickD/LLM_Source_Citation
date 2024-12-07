"""
This file will handle the loading of new documents from the sidebar.
"""

import os
import shutil
import streamlit as st
from vector_store import process_vector_store

# Constants for directories
DATA_FOLDER = "./data"
VECTOR_STORE_PATH = "./vectorstore/faiss_index.pkl"
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)


def upload_and_vectorize():
    """
    Handles the upload of new documents, deletes the old vector store,
    and re-trains the vector store while showing real-time updates in the sidebar.
    """
    with st.expander("Upload New Documents", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload TXT or PDF files", type=["txt", "pdf"], accept_multiple_files=True
        )
        upload_button = st.button("Upload and Vectorize")
        upload_placeholder = st.empty()

        if upload_button and uploaded_files:
            try:
                # Step 1: Save the uploaded files to the `data` folder
                upload_placeholder.info("Uploading files...")

                for uploaded_file in uploaded_files:
                    # Save file to the data folder
                    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        shutil.copyfileobj(uploaded_file, f)

                process_vector_store(upload_placeholder)

            except FileNotFoundError as e:
                upload_placeholder.error(f"File not found: {e}")
