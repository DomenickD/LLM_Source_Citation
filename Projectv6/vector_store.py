"""
FAISS Vector Store Management.

This script provides utility functions for managing a FAISS-based vector store
to enable efficient similarity search. It uses the `faiss` library for vector storage
and a HuggingFace embeddings model for text-to-vector representation.
"""

import pickle
import os
import subprocess
from langchain.vectorstores import FAISS
from embeddings import get_embeddings

VECTOR_STORE_FILE = "./vectorstore/faiss_index.pkl"
os.makedirs(os.path.dirname(VECTOR_STORE_FILE), exist_ok=True)


def load_local_vector_store():
    """
    Load an existing FAISS vector store from disk.

    If the vector store does not exist, this function will run `train_model.py`
    to generate a new vector store.

    Returns:
        FAISS: The loaded FAISS vector store.
    """
    embeddings = get_embeddings()

    if not os.path.exists(VECTOR_STORE_FILE):
        print("Vector store not found. Training model to create a new vector store...")
        try:
            # Run train_model.py to create the vector store
            subprocess.run(["python", "train_model.py"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to train model: {e}")

    # Load the FAISS vector store
    with open(VECTOR_STORE_FILE, "rb") as f:
        store = pickle.load(f)

    # Assign the embeddings function to the vector store
    store.embedding_function = embeddings

    print("FAISS vector store successfully loaded.")
    return store


def create_faiss_vector_store(docs):
    """
    Create a FAISS vector store from documents.

    Args:
        docs (list): List of documents to index in the vector store.

    Returns:
        FAISS: The created FAISS vector store.
    """
    embeddings = get_embeddings()
    store = FAISS.from_documents(docs, embeddings)
    save_faiss_vector_store(store)
    print("FAISS vector store created and saved.")
    return store


def save_faiss_vector_store(store):
    """
    Save the FAISS vector store to disk.

    Args:
        store (FAISS): The FAISS vector store to save.

    Returns:
        None
    """
    with open(VECTOR_STORE_FILE, "wb") as f:
        pickle.dump(store, f)
    print(f"FAISS vector store saved to {VECTOR_STORE_FILE}")


def query_faiss_vector_store(store, query_text, k=5):
    """
    Query the FAISS vector store for similar documents.

    Args:
        store (FAISS): The FAISS vector store instance.
        query_text (str): The query text to search for similar documents.
        k (int): Number of top results to retrieve.

    Returns:
        list: List of results containing similar documents.
    """
    results = store.similarity_search(query_text, k=k)
    print(f"Retrieved {len(results)} results for query: '{query_text}'")
    return results
