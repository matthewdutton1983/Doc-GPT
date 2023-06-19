# Import standard libraries
from typing import Tuple

# Import third-party libraries
import streamlit as st


class Layout:
    """Class responsible for rendering the layout of the Streamlit application."""

    def show_header(self) -> None:
        """
        Displays the header of the app
        """
        st.header("Unleash the power of conversational AI with Doc-GPT")
        st.subheader(
            "Chat with your PDF documents to get instant insights")

    def show_api_key_missing(self) -> None:
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div style='text-align: center;'>
                <h4>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI api key</a> to start chatting</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def prompt_form(self) -> Tuple[bool, str]:
        """
        Displays the prompt form

        Returns:
            Tuple[bool, str]: A tuple containing a boolean value indicating 
            whether the form is ready for submission, and a string containing 
            the user's input.
        """
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="Ask me anything about the PDF...",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input

        return is_ready, user_input
