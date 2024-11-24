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
import subprocess
import pickle

# from langchain_community.vectorstores import FAISS
from train_model import main as train_vector_store
from shared_utils import create_and_save_vector_store


# Path to save or load the FAISS vector store
VECTOR_STORE_PATH = "./vectorstore/faiss_index.pkl"
DATA_FOLDER = "./data"


def process_vector_store(upload_placeholder):
    """
    Deletes the old vector store, lists all files in the data folder,
    and retrains the vector store while updating the given placeholder.

    Args:
        upload_placeholder (streamlit.empty): The Streamlit placeholder for displaying updates.

    Returns:
        None
    """
    # Step 1: Delete the old vector store
    if os.path.exists(VECTOR_STORE_PATH):
        os.remove(VECTOR_STORE_PATH)
        upload_placeholder.info("Old vector store deleted.")

    # Step 2: List all files in the `data` folder and show in the placeholder
    data_files = os.listdir(DATA_FOLDER)
    if not data_files:
        upload_placeholder.warning(
            "No files found in the data folder. Cannot vectorize."
        )
        return

    # Step 3a: Recreate the vector store using train_model.py
    # upload_placeholder.info("Starting vectorization process...")
    # for file_name in saved_files:
    #     upload_placeholder.info(f"Vectorizing {file_name}...")
    #     time.sleep(1)  # Simulate the time it takes to process each file

    # Step 3(working)
    file_list = "\n\n".join(data_files)
    upload_placeholder.info(f"Starting vectorization process on:\n\n{file_list}")

    # Step 3: Train the new vector store
    train_vector_store()

    # Step 4: Notify success
    upload_placeholder.success("Vector store updated successfully!")


def load_local_vector_store():
    """
    Load an existing FAISS vector store from disk.

    Returns:
        FAISS: The loaded FAISS vector store object.

    Raises:
        FileNotFoundError: If the vector store file does not exist.
    """
    if not os.path.exists(VECTOR_STORE_PATH):
        print("Vector store not found. Running train_model.py to create it.")
        try:
            # Run the train_model.py script
            subprocess.run(["python", "train_model.py"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "Failed to train the model and create the vector store."
            ) from e

    with open(VECTOR_STORE_PATH, "rb") as file:
        vector_store = pickle.load(file)

    return vector_store


# def create_and_save_vector_store(documents, embeddings):
#     """
#     Create a FAISS vector store from documents and embeddings, and save it to disk.

#     Args:
#         documents (list): A list of documents to index in the vector store.
#         embeddings (Embeddings): An embeddings object for converting text into vectors.

#     Returns:
#         None

#     Side Effects:
#         Saves the created FAISS vector store to a file specified by VECTOR_STORE_PATH.
#     """

#     if not documents:
#         raise ValueError("No documents provided for vectorization.")
#     if not embeddings:
#         raise ValueError("Embeddings object is not initialized.")

#     # Create the FAISS vector store from documents and embeddings
#     vector_store = FAISS.from_documents(documents, embeddings)

#     # Ensure the output directory exists
#     output_dir = os.path.dirname(VECTOR_STORE_PATH)
#     os.makedirs(output_dir, exist_ok=True)

#     # Save the vector store to disk
#     with open(VECTOR_STORE_PATH, "wb") as file:
#         pickle.dump(vector_store, file)

#     print(f"Vector store saved to {VECTOR_STORE_PATH}")
