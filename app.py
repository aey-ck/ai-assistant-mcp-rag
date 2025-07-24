# app.py

import streamlit as st
# Import our agent classes from the new 'agents' package
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
    "Choose the agent implementation to power the chat. "
    "Notice the difference in answer quality between the two."
)

# --- Agent Selection ---
agent_type = st.sidebar.selectbox(
    "Select Agent Type:",
    ("Vector Agent (Advanced)", "Keyword Agent (Basic)")
)

# --- Agent Initialization ---
# Use st.cache_resource to load models only once
@st.cache_resource
def load_vector_agent():
    return VectorAgent(knowledge_base_path="knowledge_base.txt")

@st.cache_resource
def load_keyword_agent():
    return KeywordAgent(knowledge_base_path="knowledge_base.txt")

# Load the selected agent
if agent_type == "Vector Agent (Advanced)":
    agent = load_vector_agent()
    st.sidebar.info("Using **Vector Agent**: Understands context and meaning.")
else:
    agent = load_keyword_agent()
    st.sidebar.info("Using **Keyword Agent**: Only matches exact words.")

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am an AI Research Assistant. Select an agent and ask me a question about Mars."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and Agent Response ---
if prompt := st.chat_input("Ask a question about Mars..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get relevant info from the selected agent
            retrieved_context = agent.retrieve_relevant_info(prompt)
            
            if not retrieved_context:
                response = "I could not find any relevant information in my knowledge base to answer this question."
            else:
                # For the UI, we'll just show a clean answer.
                context_for_display = "\n- ".join(retrieved_context)
                response = (
                    f"Based on my knowledge, here is what I found about '{prompt}':\n\n"
                    f"- {context_for_display}"
                )

        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
