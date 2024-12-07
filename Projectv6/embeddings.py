"""
Embeddings Utility for Text Representation.
"""

from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """
    Initialize and return a HuggingFace embeddings object.

    Returns:
        HuggingFaceEmbeddings: An embeddings model based on the
        `sentence-transformers/all-MiniLM-L6-v2` model.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
