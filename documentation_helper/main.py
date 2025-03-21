from backend.core import run_llm
import streamlit as st
from typing import Set

# Configure the default theme to match LangChain's style
st.set_page_config(
    page_title="LangChain Documentation Helper",
    page_icon="🦜",
    layout="wide"
)

# Custom CSS to match LangChain's styling
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #0D1117;
        color: #FFFFFF;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #161B22;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Text inputs */
    .stTextInput input {
        background-color: #161B22;
        color: #FFFFFF;
        border: 1px solid #30363D;
    }
    
    /* Buttons and interactive elements */
    .stButton button {
        background-color: #238636;
        color: #FFFFFF;
        border: none;
    }
    
    /* Links */
    a {
        color: #58A6FF !important;
    }
    
    /* Divider color */
    .stDivider {
        border-color: #30363D;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #161B22;
        border: 1px solid #30363D;
    }
</style>
""", unsafe_allow_html=True)

def create_sources_string(sources:Set[str]):
    if not sources:
        return ""
    sources_list = list(sources)
    sources_list.sort()
    sources_str = "Sources:\n"
    for i,source in enumerate(sources_list):
        sources_str += f"{i + 1}. {source}\n"
        
    return sources_str

# Main content
st.header("Langchain Udemy Course Documentation Helper")

if (
    "chat_history" not in st.session_state or
    "user_inputs" not in st.session_state or
    "responses" not in st.session_state
):
    st.session_state.chat_history = []
    # NOTE: don't want to include the sources appended in the history sent to the llm
    # so need separate responses and inputs saved
    st.session_state.user_inputs = []
    st.session_state.responses = []

# Display chat messages from history on app rerun - i.e. when enter a new prompt
for user_input, response in zip(st.session_state.user_inputs, st.session_state.responses):
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(response)

if prompt := st.chat_input("What do you want to know about Langchain?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.chat_history.append(("human", prompt))
    # Add user message to user inputs displayed in UI
    st.session_state.user_inputs.append(prompt)

    with st.spinner("Generating response..."):
        res = run_llm(prompt, chat_history=st.session_state.chat_history)
        sources = set([doc.metadata["source"] for doc in res["source_documents"]])
        
        formatted_res = f"{res['result']} \n\n{create_sources_string(sources)}"
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(formatted_res)
        # Add llm response to chat history
        st.session_state.chat_history.append(("ai", res["result"]))
        # Add formatted response to stored responses displayed in UI
        st.session_state.responses.append(formatted_res)