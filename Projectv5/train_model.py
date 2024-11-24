"""
Script to Create and Save a Vector Store.

This script is used to process documents from a specified folder, generate embeddings, 
and create a vector store. The vector store is then saved for later use in applications
that require efficient similarity searches.

Modules:
- vector_store: Contains the functionality to create and save a vector store.
- embeddings: Provides the method to initialize and use embeddings for document vectors.
- document_processor: Handles document loading and splitting into manageable chunks.

Usage:
Run this script to generate and save a vector store based on the documents in the `./data` folder.
`python train_model.py`
"""

from shared_utils import create_and_save_vector_store
from embeddings import get_embeddings
from document_processor import load_and_split_documents


def main():
    """
    Main function to process documents and create a vector store.

    Workflow:
    1. Initialize embeddings for document vectorization.
    2. Load and split documents from the specified folder.
    3. Create and save a vector store using the processed documents and embeddings.

    Returns:
        None
    """
    # Initialize embeddings
    embeddings = get_embeddings()

    # Define the folder containing the documents
    data_folder = "./data"

    # Load and split documents from the data folder
    documents = load_and_split_documents(data_folder=data_folder)

    # Create and save the vector store using the documents and embeddings
    create_and_save_vector_store(documents, embeddings)


if __name__ == "__main__":
    main()
