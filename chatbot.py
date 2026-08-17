import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from .env
FREE_API_KEY = os.getenv("GROQ_API_KEY")

# Check API key
if not FREE_API_KEY:
    st.error("Groq API key not found. Please check your .env file.")
    st.stop()

# 1. Page Configuration
st.set_page_config(
    page_title="Professional AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# 2. Model Setup
def get_chat_response(messages):
    llm = ChatGroq(
        groq_api_key=FREE_API_KEY,
        model="openai/gpt-oss-120b",
        temperature=0.7
    )
    return llm.invoke(messages)


# 3. Memory Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(
            content="You are a professional, helpful, and polite AI assistant."
        )
    ]


# 4. Sidebar - Clear Chat Button
with st.sidebar:
    st.title("🤖 Chat Settings")
    st.write("Model: Llama 3.3 (Fast)")

    if st.button("Clear Conversation"):
        st.session_state.chat_history = [
            SystemMessage(
                content="You are a professional, helpful, and polite AI assistant."
            )
        ]
        st.rerun()


# 5. UI Header
st.title("🤖 Professional AI Assistant")
st.caption("Powered by Groq | Always Online")
st.markdown("---")


# 6. Display Chat History
for message in st.session_state.chat_history:

    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message.content)


# 7. User Input and AI Logic
if prompt := st.chat_input("Type your message here..."):

    # Add user message to history
    st.session_state.chat_history.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            try:
                response = get_chat_response(
                    st.session_state.chat_history
                )

                full_response = response.content

                # Display response
                st.markdown(full_response)

                # Save response to history
                st.session_state.chat_history.append(
                    AIMessage(content=full_response)
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
