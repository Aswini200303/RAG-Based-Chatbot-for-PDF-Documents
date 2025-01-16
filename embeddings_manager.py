from langchain.embeddings import HuggingFaceEmbeddings
import logging

class EmbeddingsManager:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            logging.debug("HuggingFaceEmbeddings initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize HuggingFaceEmbeddings: {e}")
            raise

    def preprocess_text_chunks(self, text_chunks):
        if not isinstance(text_chunks, list):
            logging.error(f"text_chunks should be a list but got {type(text_chunks)}.")
            raise TypeError("text_chunks must be a list.")
        return [str(chunk) for chunk in text_chunks]

    def get_embeddings(self, text_chunks):
        text_chunks = self.preprocess_text_chunks(text_chunks)
        try:
            logging.debug(f"Embedding {len(text_chunks)} text chunks.")
            return self.embeddings.embed_documents(text_chunks)
        except Exception as e:
            logging.error(f"Error embedding documents: {e}")
            raise