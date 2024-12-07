"""
Webpage Scraper and APA Citation Formatter.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DATA_FOLDER = "./data"
os.makedirs(DATA_FOLDER, exist_ok=True)


def scrape_webpage(url, output_folder=DATA_FOLDER):
    """
    Scrape text content from a webpage and save it as a text file.

    Args:
        url (str): The URL of the webpage to scrape.
        output_folder (str): The folder where the text file will be saved.

    Returns:
        str: The path to the saved text file.
    """
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    text_content = " ".join([p.get_text() for p in soup.find_all("p")])

    filename = os.path.join(
        output_folder,
        f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt",
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_content)

    return filename
