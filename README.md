# AI Research Assistant: A RAG and MCP Demonstration

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
