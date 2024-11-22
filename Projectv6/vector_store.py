"""
ChromaDB Vector Store Management.

This script provides utility functions for managing a Chroma-based vector store
to enable efficient similarity search. It uses the `chromadb` library for vector storage
and a HuggingFace embeddings model for text-to-vector representation.

Modules:
1. Configuration
2. Utility Functions
3. Example Usage
"""

import os
from langchain_chroma import Chroma  # Updated import
from embeddings import get_embeddings  # Importing custom embeddings utility

# Directory to persist Chroma data
CHROMA_DB_DIR = "./chroma_db"

# === Utility Functions ===


def initialize_chroma_vector_store(persist_directory=None):
    """
    Initialize a Chroma vector store without persistence to avoid SQLite dependency.

    Args:
        persist_directory (str, optional): Directory to persist Chroma vector store data. Defaults to None.

    Returns:
        Chroma: The initialized Chroma vector store.
    """
    # Initialize embeddings
    embeddings = get_embeddings()

    # Initialize Chroma with in-memory configuration
    store = Chroma(persist_directory=None, embedding_function=embeddings)
    print("Chroma vector store initialized in memory.")
    return store


def create_chroma_vector_store(docs, persist_directory=CHROMA_DB_DIR):
    """
    Create a Chroma vector store from documents and embeddings.

    Args:
        docs (list): List of documents to index in the vector store.
        persist_directory (str): Directory to persist Chroma vector store data.

    Returns:
        Chroma: The created Chroma vector store.
    """
    # Ensure the persistence directory exists
    os.makedirs(persist_directory, exist_ok=True)

    # Initialize the HuggingFace embeddings
    embeddings = get_embeddings()

    # Create and persist the Chroma vector store
    store = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    print(f"Chroma vector store saved to: {persist_directory}")
    return store


def query_chroma_vector_store(store, query_text, k=5):
    """
    Query the Chroma vector store for similar documents.

    Args:
        store (Chroma): The Chroma vector store instance.
        query_text (str): The query text to search for similar documents.
        k (int): Number of top results to retrieve.

    Returns:
        list: List of results containing similar documents.
    """
    results = store.similarity_search(query_text, k=k)
    print(f"Retrieved {len(results)} results for query: '{query_text}'")
    return results


# === Example Usage ===

if __name__ == "__main__":
    # Example: Documents to add to the vector store
    example_documents = [
        {"content": "The quick brown fox jumps over the lazy dog."},
        {"content": "A journey of a thousand miles begins with a single step."},
        {"content": "To be or not to be, that is the question."},
    ]

    # 1. Create and persist the vector store
    example_store = create_chroma_vector_store(example_documents)

    # 2. Load the vector store for querying
    example_store = initialize_chroma_vector_store()

    # 3. Perform a query
    example_query = "What is the meaning of life?"
    example_results = query_chroma_vector_store(example_store, example_query)

    # Display results
    for idx, result in enumerate(example_results, start=1):
        print(f"Result {idx}: {result}")
