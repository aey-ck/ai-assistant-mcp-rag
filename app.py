# app.py (Updated and Simplified)

import streamlit as st
# Import our agent classes from the 'agents' package
from agents.keyword_agent import KeywordAgent
from agents.vector_agent import VectorAgent

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Page Title and Sidebar ---
st.title("🤖 AI Research Assistant")
st.sidebar.title("Configuration")
st.sidebar.write(
    "Choose the agent implementation. The Vector Agent is now much smarter!"
)

# --- Agent Selection ---
agent_type = st.sidebar.selectbox(
    "Select Agent Type:",
    ("Vector Agent (Advanced)", "Keyword Agent (Basic)")
)

# --- Agent Initialization ---
# Use st.cache_resource to load models and data only once
@st.cache_resource
def load_vector_agent():
    """Loads the VectorAgent, caching it to avoid reloading."""
    return VectorAgent(knowledge_base_path="knowledge_base.txt")

@st.cache_resource
def load_keyword_agent():
    """Loads the KeywordAgent, caching it to avoid reloading."""
    return KeywordAgent(knowledge_base_path="knowledge_base.txt")

# Load the selected agent based on the dropdown choice
if agent_type == "Vector Agent (Advanced)":
    agent = load_vector_agent()
    st.sidebar.info("Using **Vector Agent**: Includes a classifier to understand query intent and provide more accurate responses.")
else:
    agent = load_keyword_agent()
    st.sidebar.info("Using **Keyword Agent**: A basic implementation that only matches exact words. It will fail on questions like 'who are you?'.")

# --- Chat History Management ---
# Initialize chat history in Streamlit's session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am an AI Research Assistant. Select an agent and ask me a question about Mars."}
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

    # Display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # --- Simplified Logic ---
            # Because both agents now have a .get_response() method,
            # we can call it directly without needing to check the agent type.
            # This is much cleaner and better design.
            response_data = agent.get_response(prompt)
            response = response_data['content']

        st.markdown(response)
    
    # Add the assistant's final response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

