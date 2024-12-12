"""This file houses the creating and saving 
of the vectorstore to avoid circluar imports.
"""

import os
import pickle
from langchain.vectorstores import FAISS

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
