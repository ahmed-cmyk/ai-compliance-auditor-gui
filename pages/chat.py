import streamlit as st
from langchain_ollama.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage, SystemMessage

st.title("Chat")

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TEMPERATURE = 0.7
SYSTEM_PROMPT_CONTENT = "You are a helpful, professional and friendly AI assistant. Be concise and provide accurate information."

# Session State Initialization
def initialize_session_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=SYSTEM_PROMPT_CONTENT)
        ]
    # Initialize thinking state
    if "thinking" not in st.session_state:
        st.session_state.thinking = False
    if "chat_model" not in st.session_state:
        try:
            # Initialize the chat model
            st.session_state.chat_model = ChatOllama(
                model=DEFAULT_MODEL,
                temperature=DEFAULT_TEMPERATURE,
                streaming=True
            )

        except Exception as e:
            st.error(f"Failed to initialize chat model: {str(e)}")
            st.stop()

initialize_session_state()

for message in st.session_state.messages:
    # Only display HumanMessage and AIMessage in the chat UI
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

if prompt := st.chat_input("Ask AI", disabled=st.session_state.thinking):
    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.session_state.thinking = True
        try:
            # Stream the response from the model
            full_response = ""
            message_placeholder = st.empty() # Placeholder for streaming text
            for chunk in st.session_state.chat_model.stream(st.session_state.messages):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌") # Add a blinking cursor effect
            message_placeholder.markdown(full_response) # Final display without cursor

            # Append assistant message
            st.session_state.messages.append(AIMessage(content=full_response))
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.session_state.messages.pop() # Remove the last user message if an error occurred
        finally:
            st.session_state.thinking = False # Reset thinking state
            st.rerun() # Rerun to clear input and enable it
