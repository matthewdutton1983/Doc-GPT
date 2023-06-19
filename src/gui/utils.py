# Import standard libraries
import os

# Import third-party libraries
import streamlit as st

# Import project code
from chatbot import Chatbot
from embedding import Embedder


class Utilities:
    """Utility functions for Streamlit application"""

    @staticmethod
    def load_api_key():
        """Loads the OpenAI API key from the .env file or from the user's input and returns it.

        Returns:
            str: The OpenAI API key.
        """
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
        else:
            user_api_key = st.sidebar.text_input(
                label="OpenAI API Key", placeholder="Paste your OpenAI API key here", type="password"
            )

        return user_api_key

    @staticmethod
    def handle_upload():
        """Handles the file upload and displays the uploaded file.

        Returns:
            UploadedFile or None: The uploaded file if it exists, else None.
        """
        uploaded_file = st.sidebar.file_uploader(
            "upload", type="pdf", accept_multiple_files=False, label_visibility="collapsed")

        if uploaded_file is not None:
            pass
        else:
            st.sidebar.info(
                "Upload a PDF file to get started"
            )
            st.session_state["reset_chat"] = True

        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """Sets up the chatbot with the uploaded file, model, and temperature.

        Args:
            uploaded_file (str): The path to the uploaded file.
            model (str): The model to be used by the chatbot.
            temperature (float): The temperature parameter for the chatbot's response generation.

        Returns:
            Chatbot: The initialized chatbot.
        """
        embeds = Embedder()
        with st.spinner("Processing ..."):
            # Check if uploaded_file is a string
            if isinstance(uploaded_file, str):
                # Open the file and read its content
                with open(uploaded_file, "rb") as f:
                    file = f.read()
            else:
                # If uploaded_file is a file-like object, use seek() and read()
                uploaded_file.seek(0)
                file = uploaded_file.read()

            vectors = embeds.get_doc_embeds(file)
            chatbot = Chatbot(model, temperature, vectors)
        st.session_state["ready"] = True

        return chatbot
