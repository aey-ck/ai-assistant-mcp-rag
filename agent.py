# agent.py

class AIResearchAgent:
    """
    A simple research agent that demonstrates Retrieval-Augmented Generation (RAG)
    and the principles of a Model Context Protocol (MCP).
    """

    def __init__(self, knowledge_base_path: str):
        """
        Initializes the agent with a path to its knowledge base.
        """
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        print("Agent initialized. Knowledge base loaded.")

    def _load_knowledge_base(self, path: str) -> list[str]:
        """Loads the knowledge base from a text file into a list of sentences."""
        try:
            with open(path, 'r') as f:
                # Simple strategy: split the text into sentences.
                # A more advanced retriever would use chunking and embedding.
                content = f.read()
                return [sentence.strip() for sentence in content.split('.') if sentence.strip()]
        except FileNotFoundError:
            print(f"Error: Knowledge base file not found at {path}")
            return []

    def _retrieve_relevant_info(self, query: str) -> list[str]:
        """
        The "Retrieval" part of RAG.
        Finds sentences in the knowledge base that are relevant to the query.
        
        This is a simple keyword-matching retriever. A real-world RAG system
        would use a vector database for semantic similarity search.
        """
        query_words = set(query.lower().split())
        relevant_sentences = []
        for sentence in self.knowledge_base:
            if any(word in sentence.lower() for word in query_words):
                relevant_sentences.append(sentence)
        
        print(f"\n[Retriever] Found {len(relevant_sentences)} relevant sentences for query: '{query}'")
        return relevant_sentences

    def _model_context_protocol(self, query: str, context_info: list[str]) -> str:
        """
        The "Model Context Protocol" (MCP) part.
        Assembles the final prompt for the LLM by combining system instructions,
        retrieved context, and the user's query into a structured format.
        """
        system_prompt = "You are a helpful AI Research Assistant. Your task is to answer the user's question based *only* on the provided context. If the context does not contain the answer, say 'I do not have enough information to answer this question.'"
        
        context_str = "\n".join(f"- {info}." for info in context_info)
        
        final_prompt = f"""
---------------------------------
[SYSTEM PROMPT]
{system_prompt}

[CONTEXT]
{context_str}

[USER QUESTION]
{query}
---------------------------------
        """
        print("\n[MCP] Assembled the following prompt for the LLM:")
        print(final_prompt)
        return final_prompt

    def _generate_response(self, prompt: str) -> str:
        """
        The "Generation" part of RAG.
        This function simulates sending the prompt to an LLM and getting a response.
        To keep this project simple and self-contained (no API keys needed),
        we will simulate the LLM's behavior.
        """
        # In a real application, this is where you would make an API call:
        # response = openai.Completion.create(prompt=prompt, ...)
        # return response.choices[0].text.strip()

        # --- Simulation ---
        simulated_llm_response = f"""
[Simulated LLM Output]
Based on the provided context, here is the answer to your question:
(The LLM would generate a natural language answer here based on the context)
"""
        print("\n[Generator] Simulating LLM call...")
        return simulated_llm_response

    def answer_question(self, query: str):
        """
        The main method that orchestrates the RAG + MCP process.
        """
        print(f"\n\n--- Processing new query: '{query}' ---")
        # 1. Retrieve: Find relevant information.
        retrieved_context = self._retrieve_relevant_info(query)
        
        # 2. Augment (MCP): Structure the prompt for the model.
        final_prompt = self._model_context_protocol(query, retrieved_context)
        
        # 3. Generate: Get the answer from the "LLM".
        response = self._generate_response(final_prompt)
        
        print("\n[Final Answer] The agent's response is:")
        print(response)
        return response

