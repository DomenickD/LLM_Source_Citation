"""Entry point for streamlit app v3 of project:
Segmentation and refinement"""

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from utils import load_vector_store, get_context_for_question, is_document_related

# Load precomputed vector store
vector_store = load_vector_store()

# Initialize model
llm = ChatOllama(model="llama3.1", temperature=0.2)

# Streamlit UI setup
st.title("RAG-Powered Document Query Chatbot")
st.write("Ask questions about the content in the text files in the 'data' folder.")

# Toggle to switch between document-based and conversational responses
use_vector_store = st.checkbox("Use document knowledge base", value=True)

# Set up session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [
        SystemMessage(
            content="You are a helpful assistant answering questions based on text files."
        )
    ]

# Display the chat message history
for msg in st.session_state.message_history:
    if isinstance(msg, HumanMessage):
        st.write(f"**User:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.write(f"**Bot:** {msg.content}")

# Input form for new question
with st.form(key="input_form", clear_on_submit=True):
    user_question = st.text_input("Ask a question about the content in the text files:")
    submit_button = st.form_submit_button("Submit")

# Handle form submission for question answering and citation
if submit_button and user_question:
    # Add user question to message history
    st.session_state.message_history.append(HumanMessage(content=user_question))
    # Decide if the bot should use the vector store or answer conversationally
    if use_vector_store and is_document_related(user_question):
        # Retrieve context for the question
        context, source_info = get_context_for_question(
            vector_store, user_question, k=5
        )

        # Set up prompt with context for RAG
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant answering questions based on these documents. \
                        Any quotes from the source/context, please output in quotations.",
                ),
                (
                    "human",
                    f"Use the following context to answer the question: '{context}'",
                ),
                ("human", user_question),
            ]
        )

        # Invoke the model with RAG and citation prompt
        chain = prompt | llm
        ai_response = chain.invoke({"context": context, "question": user_question})

        # Append source citation to the response
        final_response = f"{ai_response.content} \n\n*The source for this answer includes files: {source_info}.*"
    else:
        # Handle conversational response without vector store retrieval
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer the question in a conversational manner.",
                ),
                ("human", user_question),
            ]
        )
        chain = prompt | llm
        ai_response = chain.invoke({"question": user_question})

        # Append AI response to message history
        final_response = ai_response.content

    st.session_state.message_history.append(AIMessage(content=final_response))

    # Display AI response with citation
    st.write(f"**Bot:** {final_response}")
