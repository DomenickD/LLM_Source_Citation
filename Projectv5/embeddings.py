"""
Embeddings Utility for Text Representation.

This script provides a utility function to initialize and retrieve embeddings using
the HuggingFace `sentence-transformers` model. These embeddings are used for converting
text into vector representations suitable for similarity search and machine learning tasks.

Function:
- get_embeddings: Initializes and returns a HuggingFace embeddings model.

Usage:
Call `get_embeddings` to obtain an embeddings object configured with the 
`sentence-transformers/all-MiniLM-L6-v2` model.
"""

from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """
    Initialize and return a HuggingFace embeddings object.

    Returns:
        HuggingFaceEmbeddings: An embeddings model based on the
        `sentence-transformers/all-MiniLM-L6-v2` model.

    Usage:
        embeddings = get_embeddings()
        vector = embeddings.embed_query("example text")
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
