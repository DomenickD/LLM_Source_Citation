import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from utils import (
    load_vector_store,
    retrieve_from_vector_store,
    conversational_response,
    get_keywords_from_data_folder,
    generate_apa_citation,
)

# Load precomputed vector store
vector_store = load_vector_store()

# Load keywords from data folder
keywords = get_keywords_from_data_folder()


# Define the response function that combines context and model response
def generate_contextual_response(question, llm):
    # Retrieve relevant context for the question
    context, source_info = retrieve_from_vector_store(vector_store, question)

    # Extract the first source file (assuming one primary source per response)
    primary_source_file = source_info.split(",")[0].strip()

    # Generate APA citation for the source file
    apa_citation = generate_apa_citation(llm, primary_source_file)

    # Define a prompt that explicitly tells the model to use the provided context for answering
    contextual_prompt = f"""
    Use the following context to answer the question as accurately as possible based on this information:

    Context:
    {context}

    Question: {question}
    
    Answer based only on the context provided above.
    """

    # Generate response based on the context
    response = llm.invoke(contextual_prompt)

    # Extract the content of the response
    final_response_text = response.content if hasattr(response, "content") else response

    # Format the response with source information for clear citation
    final_response = f"{final_response_text}\n\n*Source: {apa_citation}*"

    return final_response


# Streamlit UI setup
st.title("RAG-Powered Document Query Chatbot")
st.write("Ask questions about the content of the files in the 'data' folder.")
st.write(
    """To query files, use "tell me about" or the name of the file in your prompt."""
)

# Settings section with st.expander
with st.expander("Model Settings"):
    # Slider to set model temperature
    TEMPERATURE = st.slider(
        "Set model temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1
    )

# Initialize the language model with the selected temperature
llm = ChatOllama(model="llama3.1", temperature=TEMPERATURE)

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

    # Decide whether to use vector store or conversational response
    if "tell me about" in user_question.lower() or any(
        keyword in user_question.lower() for keyword in keywords
    ):
        # Generate a response using the context
        final_response = generate_contextual_response(user_question, llm)
    else:
        # Directly use conversational response for general questions
        final_response = conversational_response(user_question)

    # Add response to the message history
    st.session_state.message_history.append(AIMessage(content=final_response))

    # Display the bot's response
    st.write(f"**Bot:** {final_response}")
