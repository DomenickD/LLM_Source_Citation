import os
from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Initialize LLaMA tokenizer
model_name = "facebook/llama"
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Function to extract text from text or PDF files
def extract_text_from_file(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise ValueError("Unsupported file type. Use .txt files.")


# Function to preprocess and chunk documents
def preprocess_and_chunk(text, source):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    return [{"text": chunk, "metadata": {"source": source}} for chunk in chunks]


# Function to create a vector store using FAISS
def create_vector_store(docs):
    embeddings = [
        tokenizer.encode(doc["text"], return_tensors="pt").squeeze(0).tolist()
        for doc in docs
    ]
    vector_store = FAISS.from_embeddings(
        embeddings, metadatas=[doc["metadata"] for doc in docs]
    )
    return vector_store


# Function to load documents and create vector store
def load_and_embed_documents(file_paths):
    chunks = []
    for file_path in file_paths:
        text = extract_text_from_file(file_path)
        source = os.path.basename(file_path)
        chunks.extend(preprocess_and_chunk(text, source))
    vector_store = create_vector_store(chunks)
    return vector_store
