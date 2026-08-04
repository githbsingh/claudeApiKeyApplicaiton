import streamlit as st


class ConversationMemory:

    MEMORY_KEY = "conversation_messages"

    @classmethod
    def initialize(cls):
        """
        Initialize conversation memory
        if it does not already exist.
        """

        if cls.MEMORY_KEY not in st.session_state:
            st.session_state[cls.MEMORY_KEY] = []

    @classmethod
    def add_message(
        cls,
        role: str,
        content: str
    ):
        """
        Add a message to conversation memory.
        """

        cls.initialize()

        st.session_state[
            cls.MEMORY_KEY
        ].append(
            {
                "role": role,
                "content": content
            }
        )

    @classmethod
    def get_messages(cls):
        """
        Return all conversation messages.
        """

        cls.initialize()

        return st.session_state[
            cls.MEMORY_KEY
        ]

    @classmethod
    def clear(cls):
        """
        Delete all conversation messages.
        """

        st.session_state[
            cls.MEMORY_KEY
        ] = []