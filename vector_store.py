from langchain.vectorstores import FAISS
from embeddings_manager import EmbeddingsManager

class VectorStore:
    def __init__(self):
        self.embeddings_manager = EmbeddingsManager(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    def create_vector_store(self, text_chunks):
        embeddings = self.embeddings_manager.get_embeddings(text_chunks)
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=self.embeddings_manager.embeddings)
        return vector_store