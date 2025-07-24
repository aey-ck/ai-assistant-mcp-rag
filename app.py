# app.py

import streamlit as st
from agent import AIResearchAgent # Import our agent

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Page Title and Description ---
st.title("🤖 AI Research Assistant")
st.write(
    "This app demonstrates a simple AI agent using RAG and MCP principles. "
    "Ask a question about Mars, and the agent will answer based on its local knowledge base."
)

# --- Agent Initialization ---
# We use st.cache_resource to initialize the agent only once, which is more efficient.
@st.cache_resource
def load_agent():
    """Loads the AIResearchAgent, caching it to avoid reloading on every interaction."""
    return AIResearchAgent(knowledge_base_path="knowledge_base.txt")

agent = load_agent()

# --- Chat History Management ---
# Initialize chat history in Streamlit's session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am an AI Research Assistant. How can I help you with your questions about Mars?"}
    ]

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and Agent Response ---
# Get user input from the chat input box
if prompt := st.chat_input("Ask a question about Mars..."):
    # Add user's message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the agent's response
    with st.chat_message("assistant"):
        # Use a spinner to show that the agent is "thinking"
        with st.spinner("Thinking..."):
            # We need to capture the agent's full output.
            # For this example, we'll call the agent and craft a simplified response.
            # A more advanced version would capture the print statements from the agent.
            
            retrieved_context = agent._retrieve_relevant_info(prompt)
            if not retrieved_context:
                response = "I do not have enough information to answer this question from my knowledge base."
            else:
                # For the UI, we'll just show a clean answer.
                # The full RAG/MCP process still happens in the background (and prints to terminal).
                response = (
                    f"Based on my knowledge, here is what I found about '{prompt}':\n\n"
                    f"Relevant Information:\n"
                    f"{' '.join(retrieved_context)}"
                )

        st.markdown(response)
    
    # Add agent's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

