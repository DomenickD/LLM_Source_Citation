"""Utility functiosn to support app"""

import os
import pickle
import requests
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


def is_document_related(query):
    """
    Simple check to determine if a query is document-related.
    Returns True if the query is likely document-related, False otherwise.
    You can make this more sophisticated with a custom classifier.
    """
    keywords = ["tell me about", "who", "what", "when", "where", "describe", "explain"]
    return any(keyword in query.lower() for keyword in keywords)


def scrape_webpage(url, output_folder="./data"):
    """
    Scrapes the content of a webpage and saves it as a text file in the specified folder.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the text content from the webpage
    text_content = " ".join([p.get_text() for p in soup.find_all("p")])

    # Create a unique filename based on the URL
    filename = os.path.join(
        output_folder,
        f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt",
    )

    # Save the content to a text file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_content)

    print(f"Webpage content saved to {filename}")

    # Update the vector store with the new file
    update_vector_store(data_folder=output_folder)
    return filename


def format_apa_citation(url):
    """
    Generate a simple APA citation for a webpage.
    """
    import datetime

    now = datetime.datetime.now()
    citation = f"{url}. Retrieved {now.strftime('%Y, %B %d')}."
    return citation
