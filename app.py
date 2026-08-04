import streamlit as st

from config.settings import validate_settings
from memory.conversation_memory import (
    ConversationMemory
)
from services.chat_service import ChatService


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)


validate_settings()


st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Claude on Amazon Bedrock "
    "with Conversation Memory"
)


# Initialize memory
ConversationMemory.initialize()


# Initialize Bedrock chat service
if "chat_service" not in st.session_state:

    st.session_state[
        "chat_service"
    ] = ChatService()


# Clear conversation button
if st.sidebar.button(
    "🗑️ Clear Conversation"
):

    ConversationMemory.clear()

    st.rerun()


# Display conversation history
for message in (
    ConversationMemory.get_messages()
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# Get user input
user_message = st.chat_input(
    "Ask me anything..."
)


if user_message:

    # Save user message
    ConversationMemory.add_message(
        role="user",
        content=user_message
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # Get complete history
    conversation_history = (
        ConversationMemory.get_messages()
    )


    # Generate response
    with st.chat_message("assistant"):

        with st.spinner(
            "Claude is thinking..."
        ):

            try:

                answer = (
                    st.session_state[
                        "chat_service"
                    ].chat(
                        conversation_history
                    )
                )


                st.markdown(answer)


                # Save Claude response
                ConversationMemory.add_message(
                    role="assistant",
                    content=answer
                )


            except Exception as error:

                st.error(
                    "Unable to get a response."
                )

                st.exception(error)