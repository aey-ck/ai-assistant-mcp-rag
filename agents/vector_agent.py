# agents/vector_agent.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorAgent:
    """
    An advanced agent that uses a Vector Database (FAISS) for Retrieval-Augmented
    Generation (RAG) and includes a query classifier to handle different types of questions.
    """

    def __init__(self, knowledge_base_path):
        print("Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._build_vector_db(knowledge_base_path)
        
        # Define keywords for different query types
        self.mars_keywords = ["mars", "planet", "red planet", "olympus mons", "valles marineris", "phobos", "deimos", "rover", "curiosity", "perseverance", "insight", "water", "ice", "atmosphere", "seasons", "moons"]
        self.meta_keywords = ["who are you", "what are you", "your name", "what can you do", "help"]
        self.greeting_keywords = ["hello", "hi", "hey", "greetings"]

        print("VectorAgent initialized with Query Classifier.")

    def _build_vector_db(self, path):
        # This method remains the same
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

    def _classify_query(self, query):
        """
        Classifies the user's query into one of several categories.
        This acts as a "router" to decide how to respond.
        """
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in self.meta_keywords):
            return "meta"
        if any(keyword in query_lower for keyword in self.greeting_keywords):
            return "greeting"
        if any(keyword in query_lower for keyword in self.mars_keywords):
            return "mars_topic"
            
        # If no specific keywords are found, we can use the vector DB to see
        # if the query is close to our knowledge base content. This is a more
        # advanced check for relevance.
        if self.faiss_index:
            query_vector = self.embedding_model.encode([query])
            distances, _ = self.faiss_index.search(query_vector, 1)
            # The distance is a measure of similarity. Lower is better.
            # We can set a threshold. If the closest document is still too "far",
            # then the query is likely off-topic. This threshold requires tuning.
            if distances[0][0] < 0.8: # This threshold is empirical!
                return "mars_topic"

        return "unknown"

    def retrieve_relevant_info(self, query, top_k=3):
        # This method remains the same
        if self.faiss_index is None:
            return []
            
        query_vector = self.embedding_model.encode([query])
        distances, indices = self.faiss_index.search(query_vector, top_k)
        relevant_docs = [self.documents[i] for i in indices[0]]
        return relevant_docs

    def get_response(self, query):
        """
        This is the new main entry point for the agent.
        It classifies the query first and then decides what to do.
        """
        query_type = self._classify_query(query)
        
        response_data = {'type': query_type, 'content': ""}

        if query_type == "greeting":
            response_data['content'] = "Hello! I am an AI Research Assistant focused on Mars. How can I help you?"
            return response_data

        if query_type == "meta":
            response_data['content'] = "I am an AI Research Assistant. My purpose is to answer questions about the planet Mars based on a specific knowledge base. I can tell you about its physical characteristics, missions, moons, and more."
            return response_data

        if query_type == "mars_topic":
            retrieved_context = self.retrieve_relevant_info(query)
            if not retrieved_context:
                response_data['content'] = "I found a related topic but have no specific information to answer your question."
                response_data['type'] = 'no_info' # Change type for clarity
            else:
                context_for_display = "\n- ".join(retrieved_context)
                response_data['content'] = (
                    f"Based on my knowledge, here is what I found about '{query}':\n\n"
                    f"- {context_for_display}"
                )
            return response_data

        # If the type is "unknown"
        response_data['content'] = "I'm sorry, my knowledge is limited to the planet Mars. I can't answer questions on other topics."
        return response_data
