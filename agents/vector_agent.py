# agents/vector_agent.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorAgent: # Renamed class to be specific
    """
    An advanced agent that uses a Vector Database (FAISS) for Retrieval-Augmented
    Generation (RAG) to provide accurate, context-aware answers.
    """

    def __init__(self, knowledge_base_path):
        print("Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._build_vector_db(knowledge_base_path)
        print("VectorAgent initialized. Vector DB is ready.")

    def _build_vector_db(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
                self.documents = [sentence.strip() for sentence in content.split('.') if sentence.strip()]
            
            print(f"Found {len(self.documents)} sentences in the knowledge base.")
            print("Encoding documents into vectors...")
            
            doc_vectors = self.embedding_model.encode(self.documents)
            vector_dim = doc_vectors.shape[1]
            self.faiss_index = faiss.IndexFlatL2(vector_dim)
            self.faiss_index.add(doc_vectors)
            print("FAISS index built successfully.")

        except FileNotFoundError:
            print("Error: Knowledge base file not found at " + path)
            self.documents = []
            self.faiss_index = None

    def retrieve_relevant_info(self, query, top_k=3): # Made this a public method for the app
        if self.faiss_index is None:
            return []
            
        query_vector = self.embedding_model.encode([query])
        distances, indices = self.faiss_index.search(query_vector, top_k)
        relevant_docs = [self.documents[i] for i in indices[0]]
        return relevant_docs
