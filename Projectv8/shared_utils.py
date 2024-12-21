"""This file houses the creating and saving 
of the vectorstore to avoid circluar imports.
"""

import os
import pickle
import glob
import streamlit as st
from langchain_community.vectorstores import FAISS

VECTOR_STORE_PATH = "./vectorstore/faiss_index.pkl"


def create_and_save_vector_store(documents, embeddings):
    """
    Create a FAISS vector store from documents and embeddings, and save it to disk.

    Args:
        documents (list): A list of documents to index in the vector store.
        embeddings (Embeddings): An embeddings object for converting text into vectors.

    Returns:
        None

    Side Effects:
        Saves the created FAISS vector store to a file specified by VECTOR_STORE_PATH.
    """

    if not documents:
        raise ValueError("No documents provided for vectorization.")
    if not embeddings:
        raise ValueError("Embeddings object is not initialized.")

    # Create the FAISS vector store from documents and embeddings
    vector_store = FAISS.from_documents(documents, embeddings)

    # Ensure the output directory exists
    output_dir = os.path.dirname(VECTOR_STORE_PATH)
    os.makedirs(output_dir, exist_ok=True)

    # Save the vector store to disk
    with open(VECTOR_STORE_PATH, "wb") as file:
        pickle.dump(vector_store, file)

    print(f"Vector store saved to {VECTOR_STORE_PATH}")


def display_readme(readme_path: str, img_folder_path: str):
    """
    Displays a README file with embedded images.

    Args:
        readme_path (str): Path to the README file.
        img_folder_path (str): Path to the folder containing images.
    """
    try:
        # Debug: Log the current working directory
        st.write(f"Current working directory: {os.getcwd()}")
        st.write(f"Looking for README at: {readme_path}")

        # Open the README file
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_line = f.readlines()

        readme_buffer = []
        # Get all image file names from the specified folder
        img_files = [os.path.basename(x) for x in glob.glob(f"{img_folder_path}/*")]

        for line in readme_line:
            readme_buffer.append(line)
            for image in img_files:
                if image in line:
                    st.markdown("".join(readme_buffer[:-1]))
                    st.image(f"{img_folder_path}/{image}", use_container_width=True)
                    readme_buffer.clear()

        # Render remaining buffer if any
        if readme_buffer:
            st.markdown("".join(readme_buffer))

    except FileNotFoundError:
        # Debug: Log the error
        st.error(f"README file not found at: {readme_path}")
        st.error(f"Ensure the file path is relative to: {os.getcwd()}")
