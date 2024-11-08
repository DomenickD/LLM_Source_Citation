"""https://python.langchain.com/v0.2/docs/integrations/chat/ollama/
Version 2 will stick to the documentation more.
I may have gone too far to avoid issues"""

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Initialize model and embeddings with Hugging Face model
llm = ChatOllama(model="llama3.1", temperature=0.3)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load text files from 'data' folder
data_folder = "./data"
loader = DirectoryLoader(data_folder, glob="*.txt")

# Split text into chunks using RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Load and split documents, then apply metadata
try:
    documents = loader.load_and_split(text_splitter=text_splitter)
    print("Files loaded and split successfully.")
except Exception as e:
    st.error(f"Error loading and splitting documents: {e}")
    documents = []

# Check if documents were loaded successfully
if not documents:
    st.error("No documents were loaded. Please check the files in the data folder.")
else:
    print("Looks like it worked!")
# Create vector store from document chunks
vector_store = FAISS.from_documents(documents, embeddings)
# Streamlit UI setup
st.title("RAG-Powered Document Query Chatbot")
st.write("Ask questions about the content in the text files in the 'data' folder.")

# Set up session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [
        SystemMessage(
            content="You are a helpful assistant answering \
                questions based on files you are trained."
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

    # Retrieve relevant document chunks using vector store
    docs = vector_store.similarity_search(user_question, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    source_info = ", ".join(set(doc.metadata.get("source", "unknown") for doc in docs))
    context = context[:400]
    # Set up prompt with context for RAG
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant answering questions based on these documents.",
            ),
            ("human", f"Use the following context to answer the question: '{context}'"),
            ("human", user_question),
        ]
    )

    # Invoke the model with RAG and citation prompt
    chain = prompt | llm
    ai_response = chain.invoke({"context": context, "question": user_question})

    # Append source citation to the response
    final_response = f"{ai_response.content} \n\n*The source for this answer includes files: {source_info}.*"
    st.session_state.message_history.append(AIMessage(content=final_response))

    # Display AI response with citation
    st.write(f"**Bot:** {final_response}")
