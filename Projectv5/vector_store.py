"""
Vector Store Management Utilities.

This script provides utility functions for loading and saving a FAISS-based vector store 
to enable efficient similarity search. It uses the `langchain_community` library for 
managing the FAISS vector store and `pickle` for serialization.

Functions:
- load_local_vector_store: Loads an existing FAISS vector store from disk.
- create_and_save_vector_store: Creates a FAISS vector store from documents and embeddings, and saves it to disk.

Usage:
Use `load_local_vector_store` to load a pre-existing vector store for querying.
Use `create_and_save_vector_store` to build a new vector store and save it for later use.
"""

import os
import pickle
from langchain_community.vectorstores import FAISS

# Path to save or load the FAISS vector store
VECTOR_STORE_PATH = "./vectorstore/faiss_index.pkl"


def load_local_vector_store():
    """
    Load an existing FAISS vector store from disk.

    Returns:
        FAISS: The loaded FAISS vector store object.

    Raises:
        FileNotFoundError: If the vector store file does not exist.
    """
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError("Vector store not found. Please train the model first.")

    with open(VECTOR_STORE_PATH, "rb") as file:
        vector_store = pickle.load(file)

    return vector_store


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
    # Create the FAISS vector store from documents and embeddings
    vector_store = FAISS.from_documents(documents, embeddings)

    # Ensure the output directory exists
    output_dir = os.path.dirname(VECTOR_STORE_PATH)
    os.makedirs(output_dir, exist_ok=True)

    # Save the vector store to disk
    with open(VECTOR_STORE_PATH, "wb") as file:
        pickle.dump(vector_store, file)

    print(f"Vector store saved to {VECTOR_STORE_PATH}")
