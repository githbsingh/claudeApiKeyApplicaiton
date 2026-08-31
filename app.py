import streamlit as st

from config.settings import validate_settings
from services.chat_service import ChatService


validate_settings()


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖"
)


st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Claude + Amazon Bedrock + Tool Use"
)


if "messages" not in st.session_state:

    st.session_state.messages = []


if "chat_service" not in st.session_state:

    st.session_state.chat_service = ChatService()


chat_service = st.session_state.chat_service


# ============================================================
# DISPLAY HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CLEAR
# ============================================================

if st.sidebar.button(
    "🗑️ Clear Conversation"
):

    st.session_state.messages = []

    st.rerun()


# ============================================================
# CHAT
# ============================================================

prompt = st.chat_input(
    "Ask me anything..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    with st.chat_message("assistant"):

        response = st.write_stream(

            chat_service.stream_chat(
                st.session_state.messages
            )

        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )