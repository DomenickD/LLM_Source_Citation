"""
Script to Create and Save a Vector Store.

This script is used to process documents from a specified folder, generate embeddings, 
and create a vector store. The vector store is then saved for later use in applications
that require efficient similarity searches.

Modules:
- vector_store: Contains the functionality to create and save a vector store.
- document_processor: Handles document loading and splitting into manageable chunks.

Usage:
Run this script to generate and save a vector store based on the documents in the `./data` folder.
`python train_model.py`
"""

from vector_store import create_chroma_vector_store
from document_processor import load_and_split_documents

# Define the folder containing the documents
data_folder = "./data"

# Load and split documents from the data folder
documents = load_and_split_documents(data_folder)

# Create and save the vector store using the documents
create_chroma_vector_store(documents)

# def main():
#     """
#     Main function to process documents and create a vector store.

#     Workflow:
#     1. Load and split documents from the specified folder.
#     2. Create and save a vector store using the processed documents.

#     Returns:
#         None
#     """
#     # Define the folder containing the documents
#     data_folder = "./data"

#     # Load and split documents from the data folder
#     documents = load_and_split_documents(data_folder)

#     # Create and save the vector store using the documents
#     create_chroma_vector_store(documents)


# if __name__ == "__main__":
#     main()