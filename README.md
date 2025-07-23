# A RAG and MCP Demonstration : AI Research Assistant

This project is a demonstration of a modern AI agent architecture. It implements the **Retrieval-Augmented Generation (RAG)** pattern to answer questions based on a local knowledge base, using principles from the **Model Context Protocol (MCP)** to structure the information sent to the language model.

## Core Concepts Demonstrated

1.  **Retrieval-Augmented Generation (RAG)**: The agent doesn't rely on its pre-trained knowledge. Instead, it:
    *   **Retrieves** relevant information from a local `knowledge_base.txt` file.
    *   **Augments** the user's query with this retrieved context.
    *   **Generates** an answer based *only* on the provided information, making it accurate and verifiable.

2.  **Model Context Protocol (MCP)**: Instead of just sending a blob of text to a model, the agent uses a structured protocol to assemble a clear and effective prompt. This includes:
    *   **System Instructions**: Defining the model's persona and rules.
    *   **Context**: The retrieved factual data.
    *   **User Query**: The specific question to be answered.

This approach reduces model "hallucinations" and makes the agent's behavior more predictable and reliable.

## How it Works

The agent's logic is contained in `agent.py` and follows these steps:

1.  **Load Knowledge**: The agent loads the content from `knowledge_base.txt`.
2.  **Retrieve**: When a question is asked, the retriever scans the knowledge base for relevant sentences using simple keyword matching. (In a production system, this would be a vector search).
3.  **Assemble Prompt (MCP)**: The agent constructs a detailed prompt containing the retrieved context and clear instructions for the model.
4.  **Generate**: The agent simulates a call to a Large Language Model (LLM) to generate the final answer. The simulation is used to keep the project self-contained and free of API key requirements.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Clone this repository.
3.  Run the main application from your terminal:
    ```sh
    python main.py
    ```

You will see the agent's step-by-step process printed to the console, showing how it retrieves information and constructs its prompts to answer different questions.

## Next Steps and Future Improvements

This project provides a solid foundation. The following steps could be taken to evolve it into a production-ready application:

1.  **Upgrade the Retriever with Vector Search:**
    *   **Problem:** The current retriever uses basic keyword matching and will fail if the query doesn't contain the exact words present in the knowledge base.
    *   **Solution:** Implement a semantic search retriever. This involves:
        *   Using a library like `sentence-transformers` to convert the knowledge base text into vector embeddings.
        *   Storing these embeddings in a vector database like `FAISS` (for local use) or a cloud service like `Pinecone`.
        *   Comparing the query vector with the knowledge base vectors to find the most semantically similar information.

2.  **Connect to a Real Large Language Model (LLM):**
    *   **Problem:** The generation step is currently simulated.
    *   **Solution:** Modify the `_generate_response` method in `agent.py` to make a real API call to an LLM provider.
        *   Integrate with libraries like `openai`, `google-generativeai`, or `anthropic`.
        *   Manage API keys securely using environment variables.

3.  **Add Conversation History (Memory):**
    *   **Problem:** The agent treats every question as a new, independent query. It cannot answer follow-up questions like "Why is that?"
    *   **Solution:** Enhance the Model Context Protocol (`_model_context_protocol`) to include the last few turns of the conversation, giving the agent short-term memory.

4.  **Build a User Interface:**
    *   **Problem:** Interaction is limited to the command line.
    *   **Solution:** Wrap the agent in a simple web framework to create an interactive chat interface.
        *   Use a library like `Flask` or `FastAPI` for the backend.
        *   Create a simple HTML/CSS/JavaScript frontend for users to type in their questions.
