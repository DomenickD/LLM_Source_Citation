"""Depreciated LDA page - Legacy code"""

import os
from gensim import corpora, models
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def perform_lda(data_folder="./data", num_topics=5):
    """
    Perform LDA topic modeling on the documents in the data folder.

    Args:
        data_folder (str): Path to the folder containing documents.
        num_topics (int): Number of topics to extract.

    Returns:
        dict: A dictionary with topics and associated keywords.
    """
    stop_words = set(stopwords.words("english"))
    texts = []

    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            words = [
                word.lower()
                for word in word_tokenize(text)
                if word.isalnum() and word.lower() not in stop_words
            ]
            texts.append(words)

    # Create a dictionary and corpus
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Run LDA
    lda_model = models.LdaModel(
        corpus, num_topics=num_topics, id2word=dictionary, passes=15
    )

    topics = {f"Topic {i}": lda_model.show_topic(i, topn=10) for i in range(num_topics)}
    return topics
