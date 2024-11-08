# utils.py
import os
import pickle
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_documents(data_folder, chunk_size=500, chunk_overlap=100):
    """
    Load text and PDF documents from the specified folder, split into chunks, and add metadata.
    """
    documents = []

    # Load text files
    text_loader = DirectoryLoader(data_folder, glob="*.txt")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    documents.extend(text_loader.load_and_split(text_splitter=text_splitter))

    # Load PDF files
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_folder, filename)
            pdf_loader = PyMuPDFLoader(file_path)
            pdf_documents = pdf_loader.load_and_split(text_splitter=text_splitter)

            # Add metadata for PDF source
            for doc in pdf_documents:
                doc.metadata["source"] = filename
            documents.extend(pdf_documents)

    return documents


def load_vector_store(vectorstore_path="./vectorstore/faiss_index.pkl"):
    """
    Load a precomputed vector store from disk.
    """
    with open(vectorstore_path, "rb") as f:
        vector_store = pickle.load(f)
    return vector_store


def get_context_for_question(vector_store, question, k=5):
    """
    Retrieve relevant document chunks for a given question.
    """
    docs = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    source_info = ", ".join(set(doc.metadata["source"] for doc in docs))
    return context, source_info
