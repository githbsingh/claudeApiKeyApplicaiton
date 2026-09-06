from pathlib import Path
import tempfile

import streamlit as st

from config.settings import validate_settings
from services.chat_service import ChatService
from rag.rag_service import RAGService


# ============================================================
# CONFIG
# ============================================================

validate_settings()

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Claude + Amazon Bedrock + RAG + Tool Use"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()


if "rag_service" not in st.session_state:
    st.session_state.rag_service = RAGService()


chat_service = st.session_state.chat_service
rag_service = st.session_state.rag_service


# ============================================================
# SIDEBAR - KNOWLEDGE BASE
# ============================================================

st.sidebar.header("📚 Knowledge Base")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)


if uploaded_file:

    if st.sidebar.button("📥 Ingest Document"):

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            tmp.write(
                uploaded_file.getbuffer()
            )

            temp_path = tmp.name

        try:

            with st.spinner(
                "Processing document..."
            ):

                chunk_count = rag_service.ingest(
                    temp_path
                )

            st.sidebar.success(
                f"Successfully ingested {uploaded_file.name}"
            )

        except Exception as e:

            st.sidebar.error(
                f"Ingestion failed: {e}"
            )

            st.exception(e)

        finally:

            Path(temp_path).unlink(
                missing_ok=True
            )


# ============================================================
# CLEAR CONVERSATION
# ============================================================

if st.sidebar.button(
    "🗑️ Clear Conversation"
):

    st.session_state.messages = []

    st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT
# ============================================================

prompt = st.chat_input(
    "Ask a question about the uploaded document..."
)


if prompt:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # RAG RETRIEVAL
    # --------------------------------------------------------

    retrieved_chunks = rag_service.retrieve(
        prompt,
        top_k=5
    )


    # --------------------------------------------------------
    # NO RELEVANT DOCUMENT INFORMATION
    # --------------------------------------------------------

    if not retrieved_chunks:

        answer = (
            "I couldn't find this information "
            "in the uploaded document."
        )

        with st.chat_message("assistant"):

            st.markdown(answer)


    # --------------------------------------------------------
    # DOCUMENT CONTEXT FOUND
    # --------------------------------------------------------

    else:

        grounded_prompt = rag_service.build_prompt(
            prompt,
            retrieved_chunks
        )

        with st.chat_message("assistant"):

            response = st.write_stream(
                chat_service.stream_chat(
                    [
                        {
                            "role": "user",
                            "content": grounded_prompt
                        }
                    ]
                )
            )

            answer = response


    # --------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )