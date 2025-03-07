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

# Sidebar with user profile
with st.sidebar:
    st.title("User Profile")
    
    # Add profile picture using a placeholder image
    st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y", 
             width=150,
             caption="Profile Picture")
    
    # Add name input
    user_name = st.text("Jill Villany")
    
    # Add email input
    user_email = st.text("jillvillany@gmail.com")
    
    # Add a divider
    st.divider()

# Main content
st.header("Langchain Udemy Course Documentation Helper")

prompt = st.text_input("Prompt", placeholder="Enter your question here")

if (
    "user_prompt_history" not in st.session_state
    and "chat_answers_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(sources:Set[str]):
    if not sources:
        return ""
    sources_list = list(sources)
    sources_list.sort()
    sources_str = "Sources:\n"
    for i,source in enumerate(sources_list):
        sources_str += f"{i + 1}. {source}\n"
        
    return sources_str

if prompt:
    with st.spinner("Generating response..."):
        res = run_llm(prompt, chat_history=st.session_state["chat_history"])
        sources = set([doc.metadata["source"] for doc in res["source_documents"]])
        
        formatted_res = f"{res['result']} \n\n{create_sources_string(sources)}"
        
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_res)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", res["result"]))
        
if st.session_state["chat_answers_history"]:
    for generated_res, user_prompt in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        st.chat_message("user").write(user_prompt)
        st.chat_message("assistant").write(generated_res)