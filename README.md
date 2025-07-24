# AI Research Assistant: A RAG and MCP Demonstration

This project is a demonstration of a modern AI agent architecture. It features an interactive web interface built with Streamlit and implements the **Retrieval-Augmented Generation (RAG)** pattern to answer questions based on a local knowledge base.

The agent uses principles from the **Model Context Protocol (MCP)** to structure the information sent to the language model, ensuring that its answers are grounded in facts and its behavior is predictable.


## Core Concepts Demonstrated

1.  **Retrieval-Augmented Generation (RAG)**: The agent avoids making things up by strictly following a fact-based process:
    *   **Retrieves** relevant information from a local `knowledge_base.txt` file when a question is asked.
    *   **Augments** the user's query with this retrieved context.
    *   **Generates** an answer based *only* on the provided information, making it accurate and verifiable.

2.  **Model Context Protocol (MCP)**: Instead of just sending a blob of text to a model, the agent uses a structured protocol to assemble a clear and effective prompt. This includes:
    *   **System Instructions**: Defining the model's persona and rules.
    *   **Context**: The retrieved factual data.
    *   **User Query**: The specific question to be answered.

3.  **Interactive UI**: The agent is wrapped in a user-friendly web interface using **Streamlit**, making it easy for anyone to interact with the AI without touching any code.

## Project Structure

```
.
├── .gitignore          # Specifies files for Git to ignore
├── app.py              # The Streamlit web application front-end
├── agent.py            # The core logic for the AI agent (RAG, MCP)
├── main.py             # The original command-line entry point for testing
├── knowledge_base.txt  # The agent's source of truth
├── requirements.txt    # Project dependencies (e.g., streamlit)
└── README.md           # You are here!
```

## How to Run

This project includes both an interactive web interface and a basic command-line version.

### 1. Clone the Repository

First, clone this repository to your local machine.

### 2. Install Dependencies

Navigate into the project directory and install the required Python libraries from the `requirements.txt` file:
```sh
pip install -r requirements.txt
```

### 3. Run the Interactive Web App (Recommended)

To launch the user-friendly web interface, run the following command in your terminal:
```sh
streamlit run app.py
```
A new tab should open in your web browser with the chat application. This is the best way to experience the project.

### 4. Run the Original Command-Line Version

If you want to see the detailed, step-by-step process of the agent's "thinking" printed in the terminal, you can run the original `main.py` file:
```sh
python main.py
```

---

## Next Steps and Future Improvements

This project provides a solid foundation. The following steps could be taken to evolve it into a production-ready application:

1.  **Upgrade the Retriever with Vector Search:**
    *   **Problem:** The current retriever uses basic keyword matching.
    *   **Solution:** Implement semantic search. This involves using a library like `sentence-transformers` to convert the knowledge base into vector embeddings and storing them in a vector database like `FAISS` (local) or `Pinecone` (cloud) for more intelligent searching.

2.  **Connect to a Real Large Language Model (LLM):**
    *   **Problem:** The generation step is currently simulated.
    *   **Solution:** Modify the `_generate_response` method in `agent.py` to make a real API call to an LLM provider like OpenAI, Google, or Anthropic using their respective libraries.

3.  **Add Conversation History (Memory):**
    *   **Problem:** The agent treats every question as new. It cannot answer follow-up questions like "Why is that?"
    *   **Solution:** Enhance the Model Context Protocol to include the last few turns of the conversation from Streamlit's `session_state`, giving the agent short-term memory.

4.  **✔️ Build a User Interface:**
    *   **Done!** This project already uses **Streamlit** to provide an interactive chat interface.
