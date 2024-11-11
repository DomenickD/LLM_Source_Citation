# utils.py
"""Utility functions to support app"""

import os
import pickle
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def load_and_split_documents(data_folder, chunk_size=500, chunk_overlap=100):
    """
    Load text and PDF documents from the specified folder, split into chunks, and add metadata.
    """
    documents = []

    # Ensure the data folder exists (FOR STREAMLIT CLOUD)
    if not os.path.exists(data_folder):
        return documents

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


def retrieve_from_vector_store(vector_store, question, k=5):
    """
    Retrieves context from the vector store based on the question.
    """
    docs = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    source_info = ", ".join(set(doc.metadata["source"] for doc in docs))
    return context, source_info


def conversational_response(question, temperature=0.2):
    """
    Generates a conversational response without using the vector store.
    """
    llm = ChatOllama(model="llama3.1", temperature=temperature)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a friendly conversational assistant."),
            ("human", question),
        ]
    )
    chain = prompt | llm
    ai_response = chain.invoke({"question": question})
    return ai_response.content


def is_document_related(query):
    """
    Simple check to determine if a query is document-related.
    Returns True if the query is likely document-related, False otherwise.
    You can make this more sophisticated with a custom classifier.
    """
    keywords = ["tell me about", "who", "what", "when", "where", "describe", "explain"]
    return any(keyword in query.lower() for keyword in keywords)


def generate_apa_citation(llm, filename):
    """
    Generates an APA-style citation based on the file name by prompting the LLM.
    """
    # Remove file extension and format filename as a possible citation title
    base_name = os.path.splitext(filename)[0].replace("_", " ").title()

    # Set up a prompt to ask for an APA citation based on this file name
    prompt = f"""
    Generate an APA-style citation for a document titled "{base_name}". 

    Assume the document is a classic work or historical text if the title suggests it. \
        Make reasonable inferences for author, year, and other details as needed. 
    The output should be a single-line APA-style citation only, with a brief \
        disclaimer at the end: "Citation may not be fully accurate."
    
    Example format:
    Author. (Year). Title in Title Case [Document Type]. Publisher.
    """

    # Generate the citation by invoking the LLM
    response = llm.invoke(prompt)
    citation_text = response.content if hasattr(response, "content") else response

    # Return the generated APA citation
    return citation_text


def get_keywords_from_data_folder(data_folder="./data"):
    """
    Extracts keywords based on file names in the data folder.
    """
    keywords = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt") or filename.endswith(".pdf"):
            # Extract the base name without extension, e.g., "Grimms_Fairy_Tale" -> "grimms fairy tale"
            base_name = os.path.splitext(filename)[0].replace("_", " ").lower()
            keywords.extend(base_name.split())  # Split by words for broader matching
    return set(keywords)
