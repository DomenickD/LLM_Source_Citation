"""
Document Processing Utilities for Loading, Splitting, and Context Extraction.

This script provides utility functions to load and split text and PDF documents
from a specified directory, extract context for questions using a vector store,
determine if a query is document-related, and extract keywords from file names.

Modules:
- DirectoryLoader: Handles loading `.txt` files from a directory.
- PyMuPDFLoader: Handles loading `.pdf` files.
- RecursiveCharacterTextSplitter: Splits documents into manageable chunks for processing.

Functions:
- load_and_split_documents: Loads text and PDF documents from a folder, splits them into chunks, and stores metadata.
- get_context_for_question: Retrieves relevant context for a question using a vector store.
- is_document_related: Checks if a query is related to document content.
- get_keywords_from_data_folder: Extracts keywords from file names in a specified folder.

Usage:
These functions are intended to be part of a larger document processing and query-answering system.
"""

import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_and_split_documents(input_folder: str, chunk_size=500, chunk_overlap=100):
    """
    Load and split text and PDF documents from a folder into manageable chunks.

    Args:
        data_folder (str): The path to the folder containing documents.
        chunk_size (int, optional): The size of each text chunk. Defaults to 500.
        chunk_overlap (int, optional): The overlap between consecutive chunks. Defaults to 100.

    Returns:
        list: A list of Document objects, each containing the content and metadata of a chunk.
    """
    documents_list = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    print(f"Loading documents from folder: {input_folder}")

    for root, _, files in os.walk(input_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                print(f"Processing file: {filename}")

                if filename.endswith(".txt"):
                    # Load and split TXT files
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    if not content.strip():
                        print(f"Skipping {filename}: File is empty.")
                        continue
                    chunks = text_splitter.split_text(content)
                elif filename.endswith(".pdf"):
                    # Load and split PDF files
                    pdf_loader = PyMuPDFLoader(file_path)
                    chunks = pdf_loader.load_and_split(text_splitter=text_splitter)
                else:
                    print(f"Skipping unsupported file type: {filename}")
                    continue

                if not chunks:
                    print(f"Skipping {filename}: No valid chunks extracted.")
                    continue

                # Wrap each chunk in a Document object with metadata
                for chunk in chunks:
                    doc = Document(page_content=chunk, metadata={"source": filename})
                    documents_list.append(doc)

                print(f"Processed {len(chunks)} chunks from {filename}.")

            except FileNotFoundError as e:
                print(f"Error processing {filename}: {e}")

    if not documents_list:
        print("No valid documents found in the folder.")
    return documents_list


def get_context_for_question(vector_store, question, k=5):
    """
    Retrieve relevant context and source information for a given question using a vector store.

    Args:
        vector_store (object): The vector store for similarity search.
        question (str): The query or question to search for.
        k (int, optional): The number of top documents to retrieve. Defaults to 5.

    Returns:
        tuple: A tuple containing:
            - context (str): The concatenated content of relevant documents.
            - source_info (str): A comma-separated string of document sources.
    """
    docs = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    source_info = ", ".join(set(doc.metadata["source"] for doc in docs))
    return context, source_info


def is_document_related(query):
    """
    Check if a query is likely to be related to document content.

    Args:
        query (str): The user's query or input.

    Returns:
        bool: True if the query contains keywords suggesting document-related intent, otherwise False.
    """
    keywords = ["tell me about", "who", "what", "when", "where", "describe", "explain"]
    return any(keyword in query.lower() for keyword in keywords)


def get_keywords_from_data_folder(folder="./data"):
    """
    Extract keywords from file names in the specified folder.

    Args:
        data_folder (str, optional): The path to the folder containing documents. Defaults to "./data".

    Returns:
        list: A list of keywords extracted from the base names of `.txt` and `.pdf` files in the folder.
    """
    keywords = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt") or filename.endswith(".pdf"):
            base_name = os.path.splitext(filename)[0]
            keywords.append(base_name.lower())
    return keywords


# if __name__ == "__main__":
#     data_folder = "./data"
#     documents = load_and_split_documents(data_folder)

#     if not documents:
#         print("No valid documents processed.")
#     else:
#         print(f"Successfully processed {len(documents)} chunks.")
