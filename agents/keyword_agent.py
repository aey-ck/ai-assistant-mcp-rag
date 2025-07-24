# agents/keyword_agent.py

class KeywordAgent: # Renamed class to be specific
    """
    A simple agent that uses keyword matching for Retrieval.
    This is the original, less accurate implementation kept for reference.
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

    def retrieve_relevant_info(self, query): # Made this a public method for the app
        query_words = set(query.lower().split())
        relevant_sentences = []
        for sentence in self.knowledge_base:
            if any(word in sentence.lower() for word in query_words):
                relevant_sentences.append(sentence)
        return relevant_sentences
