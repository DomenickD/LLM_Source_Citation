"""
Streamlit Application: RAG-Powered Document Query Chatbot.

This script implements a chatbot powered by Retrieval-Augmented Generation (RAG) 
to answer user questions based on content from text files in a specified folder. 
The chatbot supports document-based queries and general conversational responses.

Functions:
- initialize_ui: Sets up the Streamlit user interface and allows users to configure model settings.
- initialize_model: Initializes the language model with specified parameters.
- handle_user_input: Processes user questions, retrieves context if document-related, and generates responses.
- handle_conversational_response: Handles general conversational queries not tied to documents.

Usage:
Run the script to launch the Streamlit app. Users can query text files in the `data` folder or 
engage in general conversation with the chatbot.
"""

import time
import requests
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from document_processor import get_context_for_question
from utils import scrape_webpage
from document_uploader import upload_and_vectorize


def initialize_ui():
    """
    Initialize the Streamlit user interface.

    Returns:
        float: The temperature setting for the model, which controls response randomness.
    """
    st.title("RAG-Powered Document Query Chatbot")
    st.write("Ask questions about the content in the text files in the 'data' folder.")

    st.sidebar.header("Additional Features")

    # Sidebar: Model Settings Expander
    with st.sidebar.expander("Model Settings", expanded=False):
        temperature = st.slider(
            "Set model temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1
        )

    # Sidebar: Web Scraping Expander
    with st.sidebar.expander("Scrape a Website", expanded=False):
        with st.form(key="scrape_form"):
            url_to_scrape = st.text_input("Enter a website URL:")
            scrape_button = st.form_submit_button("Scrape Website")

        # Placeholder for dynamic message display
        upload_placeholder = st.empty()

        # Handle web scraping
        if scrape_button and url_to_scrape:
            try:
                scraped_file = scrape_webpage(
                    url_to_scrape,
                    upload_placeholder=upload_placeholder,
                    output_folder="./data",
                )
                st.session_state.scrape_message = (
                    f"Scraped content saved as: {scraped_file}"
                )
            except requests.exceptions.RequestException as e:
                st.session_state.scrape_message = f"Network error: {e}"
            except ValueError as e:
                st.session_state.scrape_message = f"Data parsing error: {e}"

            # Display the message and implement the countdown
            start_time = time.time()
            while time.time() - start_time < 5:
                remaining_time = int(5 - (time.time() - start_time))
                upload_placeholder.info(
                    f"{st.session_state.scrape_message} (Closing in {remaining_time}s)"
                )
                time.sleep(1)  # Update every second

            # Clear the message after 5 seconds
            upload_placeholder.empty()
            del st.session_state.scrape_message

    # Sidebar: Document Upload
    upload_and_vectorize()

    return temperature


def initialize_model(temperature):
    """
    Initialize the language model.

    Args:
        temperature (float): The temperature setting for response randomness.

    Returns:
        ChatOllama: An instance of the ChatOllama model.
    """
    from langchain_ollama import ChatOllama

    return ChatOllama(model="llama3.1", temperature=temperature)


def handle_user_input(llm, vector_store, keywords):
    """
    Handle user input and generate responses based on queries.

    Args:
        llm (ChatOllama): The language model instance.
        vector_store (VectorStore): The vector store for document-based queries.
        keywords (list): A list of keywords from the document data folder.

    Side Effects:
        Updates the session state with user and bot messages.
        Displays responses in the Streamlit app.
    """
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            SystemMessage(
                content="You are a helpful assistant answering questions based on text files."
            )
        ]

    # Display the message history
    for msg in st.session_state.message_history:
        if isinstance(msg, HumanMessage):
            st.write(f"**User:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.write(f"**Bot:** {msg.content}")

    # Input form
    with st.form(key="input_form", clear_on_submit=True):
        user_question = st.text_input(
            "Ask a question about the content in the text files:"
        )
        submit_button = st.form_submit_button("Submit")

    if submit_button and user_question:
        st.session_state.message_history.append(HumanMessage(content=user_question))

        if "tell me about" in user_question.lower() or any(
            keyword in user_question.lower() for keyword in keywords
        ):
            # Generate a response using document context
            context, source_info = get_context_for_question(
                vector_store, user_question, k=5
            )
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a helpful assistant answering questions based on these documents.",
                    ),
                    (
                        "human",
                        f"Use the following context to answer the question: '{context}'",
                    ),
                    ("human", user_question),
                ]
            )
            chain = prompt | llm
            ai_response = chain.invoke({"context": context, "question": user_question})
            final_response = f"{ai_response.content} \n\n*Source: {source_info}*"
        else:
            # General conversational response
            final_response = handle_conversational_response(llm, user_question)

        st.session_state.message_history.append(AIMessage(content=final_response))
        st.write(f"**Bot:** {final_response}")


def handle_conversational_response(llm, user_question):
    """
    Handle conversational queries not related to documents.

    Args:
        llm (ChatOllama): The language model instance.
        user_question (str): The user's query.

    Returns:
        str: The response content generated by the model.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer in a conversational manner.",
            ),
            ("human", user_question),
        ]
    )
    chain = prompt | llm
    ai_response = chain.invoke({"question": user_question})
    return ai_response.content
