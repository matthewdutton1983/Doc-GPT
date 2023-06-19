# Import third-party libraries
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from streamlit_chat import message


class ChatHistory:
    """Class for managing chat history within a Streamlit application"""

    def __init__(self):
        """Initializes the ChatHistory class with a chat history from session state or a new one if it does not exist."""
        self.history = st.session_state.get("history",
                                            ConversationBufferMemory(memory_key="chat_history", return_messages=True))
        st.session_state["history"] = self.history

    def default_greeting(self) -> str:
        """
        Returns the default greeting message.

        Returns:
            str: Default greeting message.
        """
        return "Hi! 👋"

    def default_prompt(self, topic: str) -> str:
        """
        Returns the default prompt message, with the provided topic.

        Args:
            topic (str): Topic to be included in the default prompt message.

        Returns:
            str: Default prompt message.
        """
        return f"Hello! Ask me anything about {topic} 🤗"

    def initialize(self, topic: str) -> None:
        """
        Initializes the chat with default greeting and prompt messages.

        Args:
            topic (str): Topic to be included in the default prompt message.
        """
        message(self.default_greeting(), key='hi',
                avatar_style="thumbs", is_user=True)
        message(self.default_prompt(topic), key='ai')

    def reset(self) -> None:
        """
        Resets the chat history.
        """
        st.session_state["history"].clear()
        st.session_state["reset_chat"] = False

    def generate_messages(self, container) -> None:
        """
        Generates the messages from chat history into the provided container.

        Args:
            container (DeltaGenerator): Streamlit's DeltaGenerator object where the messages are to be displayed.
        """
        if st.session_state["history"]:
            with container:
                messages = st.session_state["history"].chat_memory.messages
                for i in range(len(messages)):
                    msg = messages[i]
                    if isinstance(msg, HumanMessage):
                        message(
                            msg.content,
                            is_user=True,
                            key=f"{i}_user",
                            avatar_style="thumbs",
                        )
                    elif isinstance(msg, AIMessage):
                        message(msg.content, key=str(i))
