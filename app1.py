import os
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import load_and_embed_documents, preprocess_and_chunk

# Load LLaMA tokenizer and model
model_name = "facebook/llama"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize session state for chat history and vector store
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "vector_store" not in st.session_state:
    file_paths = ["data/Grimms_Fairy_Tale.txt"]  # Replace with actual file paths
    st.session_state["vector_store"] = load_and_embed_documents(file_paths)

st.title("LLaMA Model with Source Citations")
st.write("Chat with LLaMA below:")


def get_response_with_retrieval(history, vector_store):
    query = history[-1]["content"]
    docs = vector_store.similarity_search(query, k=1)
    context = " ".join([doc["text"] for doc in docs])
    context = context[:300]

    # Prepare input for the model with context
    input_text = f"{context}\nUser: {query}\nAssistant:"
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate response
    outputs = model.generate(
        **inputs, max_length=150, pad_token_id=tokenizer.eos_token_id
    )
    model_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    citations = "\n\nCitations:\n" + "\n".join(
        [f"- {doc['metadata']['source']}" for doc in docs]
    )
    return model_response + citations


# Streamlit UI for sending messages
if st.button("Send"):
    if st.session_state["input_text"]:
        st.session_state["chat_history"].append(
            {"role": "user", "content": st.session_state["input_text"]}
        )
        response = get_response_with_retrieval(
            st.session_state["chat_history"], st.session_state["vector_store"]
        )
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": response}
        )
        st.session_state["input_text"] = ""

# Display chat history
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"You: {chat['content']}")
    else:
        st.write(f"LLaMA: {chat['content']}")

user_input = st.text_input("Your Message:", key="input_text")
