"""
Webpage Scraper and APA Citation Formatter.

This script provides functionality to scrape a webpage's text content, save it as a local file,
and generate an APA-style citation for the webpage. It uses the `requests` library for HTTP
requests, `BeautifulSoup` for HTML parsing, and the `datetime` module for citation formatting.

Functions:
- scrape_webpage: Downloads text content from a webpage and saves it as a `.txt` file.
- format_apa_citation: Generates an APA-style citation for the provided URL.

Usage:
Call `scrape_webpage` with the URL of the webpage to scrape its content and save it locally.
Use `format_apa_citation` to generate a formatted citation for the scraped webpage.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from vector_store import create_and_save_vector_store
from document_processor import load_and_split_documents
from embeddings import get_embeddings


def scrape_webpage(url, output_folder="./data"):
    """
    Scrape text content from a webpage and save it as a text file.

    Args:
        url (str): The URL of the webpage to scrape.
        output_folder (str, optional): The folder where the text file will be saved.
                                       Defaults to "./data".

    Returns:
        str: The path to the saved text file.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    # Send a GET request to the provided URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP request issues

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text content from all <p> tags
    text_content = " ".join([p.get_text() for p in soup.find_all("p")])

    # Create a unique filename based on the URL
    filename = os.path.join(
        output_folder,
        f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt",
    )

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write the extracted text content to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text_content)

    print(f"Webpage content saved to {filename}")

    # Update vector store with the new document
    print("Updating the vector store...")
    documents = load_and_split_documents(output_folder)
    embeddings = get_embeddings()
    create_and_save_vector_store(documents, embeddings)
    print("Vector store updated successfully!")

    return filename


def format_apa_citation(url):
    """
    Generate an APA-style citation for the provided URL.

    Args:
        url (str): The URL of the webpage to cite.

    Returns:
        str: A formatted APA-style citation.
    """
    # Get the current date
    now = datetime.now()

    # Format and return the citation
    return f"{url}. Retrieved {now.strftime('%Y, %B %d')}."


# Example usage (optional for standalone testing)
if __name__ == "__main__":
    example_url = "https://example.com"
    output_file = scrape_webpage(example_url)
    citation = format_apa_citation(example_url)
    print("APA Citation:", citation)
