import os
import shutil
import streamlit as st
from utils import scrape_webpage
from vector_store import create_faiss_vector_store
from document_processor import load_and_split_documents

DATA_FOLDER = "./data"
os.makedirs(DATA_FOLDER, exist_ok=True)


def render_upload_and_scraper_page():
    """
    Render the document upload and web-scraping functionalities on a separate page.
    """
    st.title("Upload & Web Scraper")

    # Document Upload Section
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload TXT or PDF files", type=["txt", "pdf"], accept_multiple_files=True
    )
    if st.button("Upload and Vectorize"):
        try:
            st.info("Uploading files...")
            for uploaded_file in uploaded_files:
                file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(uploaded_file, f)

            # Load and vectorize documents
            documents = load_and_split_documents(DATA_FOLDER)
            create_faiss_vector_store(documents)
            st.success("Files successfully uploaded and vectorized.")
        except Exception as e:
            st.error(f"Error during upload and vectorization: {e}")

    # Web Scraper Section
    st.subheader("Web Scraper")
    url = st.text_input("Enter a URL to scrape:")
    if st.button("Scrape Webpage"):
        if url:
            try:
                output_file = scrape_webpage(url)
                st.success(f"Webpage scraped and saved to: {output_file}")
            except Exception as e:
                st.error(f"Error during web scraping: {e}")
        else:
            st.warning("Please enter a valid URL.")
