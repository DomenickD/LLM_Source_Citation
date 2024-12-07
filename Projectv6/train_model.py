"""
Script to Create and Save a Vector Store.

This script processes documents from a specified folder, generates embeddings, 
and creates a FAISS vector store. The vector store is then saved for later use.
"""

from vector_store import create_faiss_vector_store

# from embeddings import get_embeddings
from document_processor import load_and_split_documents

DATA_FOLDER = "./data"


def main():
    """
    Main function to process documents and create a FAISS vector store.
    """
    # Initialize embeddings
    # embeddings = get_embeddings()

    # Load and split documents
    documents = load_and_split_documents(DATA_FOLDER)

    # Create and save the vector store
    create_faiss_vector_store(documents)


if __name__ == "__main__":
    main()
