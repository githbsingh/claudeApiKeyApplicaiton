import streamlit as st

from config.settings import validate_settings
from services.chat_service import ChatService


# ============================================================
# SETTINGS
# ============================================================

validate_settings()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="centered",
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Powered by Claude through Amazon Bedrock"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CHAT SERVICE
# ============================================================

if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()


chat_service = st.session_state.chat_service


# ============================================================
# DISPLAY CONVERSATION
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# CLEAR CHAT
# ============================================================

if st.sidebar.button("🗑️ Clear Conversation"):

    st.session_state.messages = []

    st.rerun()


# ============================================================
# USER INPUT
# ============================================================

prompt = st.chat_input(
    "Ask me anything..."
)


if prompt:

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    # --------------------------------------------------------
    # Generate streaming response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        response = st.write_stream(
            chat_service.stream_chat(
                st.session_state.messages
            )
        )

    # --------------------------------------------------------
    # Save complete assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )