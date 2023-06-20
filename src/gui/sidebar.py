# Import standard libraries
import os

# Import third-party libraries
import openai
import streamlit as st

openai.api_key = os.environ["OPENAI_API_KEY"]


class Sidebar:
    """Class for managing the sidebar of the Streamlit application."""
    models_list = openai.Model.list()

    MODEL_OPTIONS = [model["id"] for model in models_list["data"]]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.5
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        """Display information about the application and its dependencies."""
        about = st.sidebar.expander("About", expanded=False)
        sections = [
            "#### Powered by: [Langchain](https://github.com/hwchase17/langchain), "
            "[OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and "
            "[Streamlit](https://github.com/streamlit/streamlit)",
            "#### Source code : [GitHub](https://github.com/matthewdutton1983/Doc-GPT)",
        ]
        for section in sections:
            about.write(section)

    def model_selector(self):
        """Display radio buttons to select the AI model to be used."""
        model = st.selectbox(
            label="Model", options=self.MODEL_OPTIONS, index=13)
        st.session_state["model"] = model

    @staticmethod
    def reset_chat_button():
        """Display a button to reset the chat."""
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def temperature_slider(self):
        """Display a slider to set the "temperature" for the AI model's responses."""
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP
        )
        st.session_state["temperature"] = temperature

    def show_options(self):
        """Display a set of tools for interacting with the chat."""
        with st.sidebar.expander("Tools", expanded=False):
            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault(
                "temperature", self.TEMPERATURE_DEFAULT_VALUE)
