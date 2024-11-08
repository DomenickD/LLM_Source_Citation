# train_model.py
import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import load_and_split_documents

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load and split documents, then create vector store
data_folder = "./data"
documents = load_and_split_documents(data_folder)

# Create vector store and save it
vector_store = FAISS.from_documents(documents, embeddings)
output_dir = "./vectorstore"
os.makedirs(output_dir, exist_ok=True)

# Save vector store to disk
with open(os.path.join(output_dir, "faiss_index.pkl"), "wb") as f:
    pickle.dump(vector_store, f)

print("Vector store created and saved in vectorstore/faiss_index.pkl")
