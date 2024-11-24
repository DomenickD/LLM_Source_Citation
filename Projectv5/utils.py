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
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from vector_store import process_vector_store


def scrape_webpage(url, upload_placeholder, output_folder="./data"):
    """
    Scrape text content from a webpage, save it as a text file, and update the vector store.

    Args:
        url (str): The URL of the webpage to scrape.
        upload_placeholder (streamlit.empty): The Streamlit placeholder for displaying updates.
        output_folder (str, optional): The folder where the text file will be saved.
                                       Defaults to "./data".

    Returns:
        str: The path to the saved text file.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    try:
        # Step 1: Send a GET request to the provided URL
        upload_placeholder.info("Fetching webpage content...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raise an error for HTTP request issues

        # Step 2: Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = " ".join([p.get_text() for p in soup.find_all("p")])

        # Step 3: Create a safe and descriptive filename
        sanitized_url = (
            url.replace("http://", "").replace("https://", "").replace("/", "_")
        )
        base_name = sanitized_url.split("?")[0].split("#")[
            0
        ]  # Remove query strings and fragments
        filename = os.path.join(output_folder, f"{base_name}.txt")

        # Step 4: Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Step 5: Write the extracted text content to the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text_content)

        upload_placeholder.success(f"Webpage content saved to: {filename}")

        # Step 6: Update the vector store using the reusable function
        process_vector_store(upload_placeholder)

        return filename

    except requests.exceptions.RequestException as e:
        upload_placeholder.error(f"Failed to fetch webpage: {e}")
        raise
    except Exception as e:
        upload_placeholder.error(f"An error occurred: {e}")
        raise


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
