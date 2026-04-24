from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_DB = None

def embed_texts(texts):
    return model.encode(texts).tolist()

def create_vector_store(news_data):
    global VECTOR_DB

    documents = []
    for item in news_data:
        documents.append(
            Document(
                page_content=item["content"],
                metadata={
                    "company": item["company"],
                    "sentiment": item["sentiment"],
                    "emotion": item["emotion"],
                    "date": item["date"]
                }
            )
        )

    VECTOR_DB = FAISS.from_documents(
        documents,
        embedding=lambda x: embed_texts(x)
    )

    VECTOR_DB.save_local("faiss_index")
    return "Vector store created successfully"
