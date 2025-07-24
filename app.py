# app.py

import streamlit as st
from agents.keyword_agent import KeywordAgent # Keyword agent remains for comparison
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
@st.cache_resource
def load_vector_agent():
    return VectorAgent(knowledge_base_path="knowledge_base.txt")

@st.cache_resource
def load_keyword_agent():
    return KeywordAgent(knowledge_base_path="knowledge_base.txt")

if agent_type == "Vector Agent (Advanced)":
    agent = load_vector_agent()
    st.sidebar.info("Using **Vector Agent**: Includes a classifier to understand query intent and provide more accurate responses.")
else:
    agent = load_keyword_agent()
    st.sidebar.info("Using **Keyword Agent**: A basic implementation that only matches exact words.")

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
            # --- This is the updated logic ---
            if agent_type == "Vector Agent (Advanced)":
                # The new agent has a smarter response method
                response_data = agent.get_response(prompt)
                response = response_data['content']
            else:
                # The old agent still uses the simple retrieval method
                retrieved_context = agent.retrieve_relevant_info(prompt)
                if not retrieved_context:
                    response = "I could not find any relevant information."
                else:
                    context_for_display = "\n- ".join(retrieved_context)
                    response = (
                        f"Based on my knowledge, here is what I found:\n\n"
                        f"- {context_for_display}"
                    )

        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
