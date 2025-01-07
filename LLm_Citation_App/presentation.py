"""
This page is for presentation purposes.

It goes over what went into making this app
"""

import streamlit as st
from shared_utils import display_readme


def about_page():
    """
    Renders the "About" page for the LLM RAG app.
    """
    st.title("Behind the Scenes")
    st.caption("This app was devloped by: Domenick (Dobby) Dobbs")
    st.caption("Under the guidance of the esteemed Brett Waugh")

    st.divider()

    st.subheader("What went into the app")

    st.write(
        """
        This app is a locally hosted **Retrieval-Augmented Generation (RAG)** \
            system powered by the LLAMA model from META.
        It combines the power of large language models with custom document \
            retrieval to provide contextually relevant and accurate answers \
            to your queries.
        """
    )

    with st.expander("📘📚 **Technical Glossary** 📚📘", expanded=True):
        st.write(
            """
        Below are explanations for technical terms used in this app, aimed at a non-technical audience:
        """
        )
        st.markdown(
            """
    | **Term**                  | **Description**        |
    |---------------------------|-------------------------|
    | **LLM (Large Language Model)** | A type of AI model trained on vast \
        amounts of text data to generate and understand human language. |
    | **RAG (Retrieval-Augmented Generation)** | A method that combines \
        retrieving relevant information with generating answers, ensuring \
            the responses are accurate and context-aware. |
    | **FAISS (Facebook AI Similarity Search)** | A library used for fast \
        and efficient similarity searches across large datasets, enabling \
            document retrieval. |
    | **Vector Store**          | A database where text is converted into \
        numerical representations (vectors) to allow for similarity searches. |
    | **Topic Modeling**        | The process of discovering abstract \
        topics in a set of documents.              |
    | **Web Scraper**           | A tool that extracts text and \
        information from web pages for analysis and processing. |
    | **Embedding**             | A way of representing text or \
        data as numerical vectors, making it easier for computers\
              to process and compare. |
    | **Inference**             | The process of using a trained \
        AI model to generate predictions or answers based on input data. |
    | **Streamlit**             | A Python library for building \
        interactive and user-friendly web applications.  |
    """,
            unsafe_allow_html=True,
        )

    # Features
    st.subheader("Features")
    with st.expander(" 📄🛠️ **Document Upload and Processing** 🛠️📄"):
        st.write(
            """
            - Allows users to upload text (`.txt`) and PDF (`.pdf`) documents.
            - Automatically vectorizes documents and stores them for fast retrieval\
            in something called a vector store.
            - Supports efficient similarity search using FAISS \
                (Facebook AI Similarity Search).
            """
        )

    with st.expander("🌐🔍 **Web Scraping and Querying** 🔍🌐"):
        st.write(
            """
            - Includes a web scraper to extract content from public URLs.
            - The data is then saved as a `.txt` file.
            - Scraped data (in the text file) is added to the document \
                store so we can query it.
            - Enables real-time querying across local and web-based content.
            """
        )

    with st.expander("❓🦙 **Question-Answering with LLAMA** 🦙❓"):
        st.write(
            """
            - Integrates the **LLAMA model** (version 3.2) for generating contextually relevant answers.
            - Uses **retrieval-augmented generation (RAG)** to enhance accuracy by \
                incorporating user-provided data.
            - Dynamically adjusts responses based on the retrieved context from the vector store.
            """
        )

    with st.expander("🖥️🚀 **Want to try this app on your own computer?** 🚀🖥️"):
        display_readme("HOW_TO.md", "Pictures")

    # Benefits
    st.subheader("Benefits of a Locally Hosted App")
    st.write(
        """
        Hosting this app locally offers several advantages:
        - **Data Privacy**: Your documents and queries stay on your machine, \
            ensuring complete data security.
        - **No API Costs**: Unlike cloud-based solutions, this app does not \
            rely on paid APIs, reducing operational costs.
        - **Customizability**: Modify and extend the app to fit your specific \
            needs without external constraints.
        """
    )

    # Lessons Learned
    st.subheader("What I Learned")
    st.write(
        """
        Developing this app provided valuable insights into:
        - **Integrating LLMs with external data sources**: Learned how to \
            combine language models with retrieval-based systems.
        - **Efficient vector storage**: Used FAISS for fast similarity \
            searches over custom datasets.
        - **Streamlit for interactive UIs**: Built a user-friendly \
            interface with dynamic visualizations.
        - **Topic modeling and LDA**: Gained experience in implementing and \
            visualizing unsupervised learning techniques.
        - **Local hosting advantages**: Understood the value of privacy and \
            independence in machine learning applications.
        """
    )

    # Closing Note
    st.subheader("Conclusion and Recognition")
    st.write(
        "Thank you for exploring this app! \
        I want to give a special thank you to Brett Waugh for \
            all the work he put into leading the DS side of this RA program."
    )
    if st.button("We Did it!!!!!"):
        st.balloons()
