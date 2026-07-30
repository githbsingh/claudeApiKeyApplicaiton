import streamlit as st

from config.settings import validate_settings
from services.chat_service import ChatService


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)

validate_settings()

st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Powered by Claude on Amazon Bedrock"
)


if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
user_message = st.chat_input(
    "Ask me anything..."
)


if user_message:

    # Store and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)


    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Claude is thinking..."):

            try:

                answer = (
                    st.session_state
                    .chat_service
                    .chat(user_message)
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error(
                    f"Unable to get a response: {error}"
                )