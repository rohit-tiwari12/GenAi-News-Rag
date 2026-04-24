import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.index = None
        self.documents = []
        self.embeddings = None

    def add_documents(self, docs):
        """
        Store documents and build FAISS index
        """
        if not docs:
            return

        texts = [d["content"] for d in docs]

        # Convert text → TF-IDF vectors
        embeddings = self.vectorizer.fit_transform(texts).toarray().astype("float32")

        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])

        self.index.add(embeddings)

        self.embeddings = embeddings
        self.documents.extend(docs)

    def search(self, query, k=3):
        """
        Search similar documents for a query
        """
        if self.index is None or not self.documents:
            return []

        query_vec = self.vectorizer.transform([query]).toarray().astype("float32")

        distances, indices = self.index.search(query_vec, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results