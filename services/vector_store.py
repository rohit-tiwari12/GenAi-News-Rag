import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

    def add_documents(self, docs):
        """
        Store documents and build FAISS index
        """
        if not docs:
            return

        texts = [d["content"] for d in docs]
        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query, k=3):
        """
        Search similar documents for a query
        """
        if self.index is None or not self.documents:
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results
