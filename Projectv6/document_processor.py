"""
Document Processing Utilities for Loading, Splitting, and Context Extraction.

This script provides utility functions to load and split text and PDF documents 
from a specified directory, extract context for questions using a vector store.
"""

import os
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_documents(data_folder, chunk_size=500, chunk_overlap=100):
    """
    Load and split text and PDF documents from a folder into manageable chunks.

    Args:
        data_folder (str): The path to the folder containing documents.
        chunk_size (int, optional): The size of each text chunk. Defaults to 500.
        chunk_overlap (int, optional): The overlap between consecutive chunks. Defaults to 100.

    Returns:
        list: A list of document chunks, where each chunk is a dictionary containing the content and metadata.
    """
    documents = []

    # Load and split text files
    text_loader = DirectoryLoader(data_folder, glob="*.txt")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    documents.extend(text_loader.load_and_split(text_splitter=text_splitter))

    # Load and split PDF files
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_folder, filename)
            pdf_loader = PyMuPDFLoader(file_path)
            pdf_documents = pdf_loader.load_and_split(text_splitter=text_splitter)
            for doc in pdf_documents:
                doc.metadata["source"] = filename  # Add source metadata
            documents.extend(pdf_documents)

    return documents


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
