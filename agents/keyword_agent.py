# agents/keyword_agent.py

class KeywordAgent:
    """
    A simple agent that uses keyword matching for Retrieval.
    This is the original, less accurate implementation kept for reference.
    It now has a get_response method to maintain a consistent interface
    with the more advanced VectorAgent.
    """

    def __init__(self, knowledge_base_path):
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        print("KeywordAgent initialized.")

    def _load_knowledge_base(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
                return [sentence.strip() for sentence in content.split('.') if sentence.strip()]
        except FileNotFoundError:
            print("Error: Knowledge base file not found at " + path)
            return []

    def retrieve_relevant_info(self, query):
        query_words = set(query.lower().split())
        relevant_sentences = []
        for sentence in self.knowledge_base:
            if any(word in sentence.lower() for word in query_words):
                relevant_sentences.append(sentence)
        return relevant_sentences

    # --- ADD THIS NEW METHOD ---
    def get_response(self, query):
        """
        The main entry point for the KeywordAgent.
        This provides a consistent interface with the VectorAgent.
        """
        response_data = {'type': 'keyword_search', 'content': ""}
        
        retrieved_context = self.retrieve_relevant_info(query)
        
        if not retrieved_context:
            response_data['content'] = "I could not find any documents matching your keywords."
        else:
            context_for_display = "\n- ".join(retrieved_context)
            response_data['content'] = (
                f"Based on keyword matching, here is what I found:\n\n"
                f"- {context_for_display}"
            )
            
        return response_data
