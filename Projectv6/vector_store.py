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

from langchain_chroma import Chroma  # Updated import
from embeddings import get_embeddings  # Importing custom embeddings utility


# === Utility Functions ===


def initialize_chroma_vector_store():
    """
    Initialize a Chroma vector store without persistence to avoid SQLite dependency.

    Returns:
        Chroma: The initialized Chroma vector store.
    """
    # Initialize embeddings
    embeddings = get_embeddings()

    # Initialize Chroma in memory (no persistence)
    store = Chroma(embedding_function=embeddings)
    print("Chroma vector store initialized in memory.")
    return store


def create_chroma_vector_store(docs):
    """
    Create a Chroma vector store from documents without persistence.

    Args:
        docs (list): List of documents to index in the vector store.

    Returns:
        Chroma: The created Chroma vector store.
    """
    # Initialize the HuggingFace embeddings
    embeddings = get_embeddings()

    # Create the Chroma vector store (in-memory)
    store = Chroma.from_documents(docs, embeddings)
    print("Chroma vector store created in memory.")
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

    # 1. Create the vector store (in-memory)
    example_store = create_chroma_vector_store(example_documents)

    # 2. Perform a query
    example_query = "What is the meaning of life?"
    example_results = query_chroma_vector_store(example_store, example_query)

    # Display results
    for idx, result in enumerate(example_results, start=1):
        print(f"Result {idx}: {result}")
