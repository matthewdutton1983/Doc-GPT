# Import standard libraries
import os
import traceback
from tempfile import NamedTemporaryFile

# Import third-party libraries
import streamlit as st
from pdf2image import convert_from_path

# Import project code
from gui.history import ChatHistory
from gui.layout import Layout
from gui.sidebar import Sidebar
from gui.utils import Utilities

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_icon="💬", page_title="Doc-GPT")

    layout, sidebar, utils = Layout(), Sidebar(), Utilities()
    layout.show_header()
    user_api_key = utils.load_api_key()

    if not user_api_key:
        layout.show_api_key_missing()
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        uploaded_file = utils.handle_upload()

        if uploaded_file:
            # Create a temporary file and write the uploaded file's bytes to it
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
                tmp_name = tmp_file.name.split("/")[-1]

            pdf_column, chatbot_column = st.columns((1.5, 1))

            # Render the PDF as images and display on the left
            with pdf_column:
                images = convert_from_path(
                    tmp_path, poppler_path=os.getenv("POPPLER_PATH"))
                for i, image in enumerate(images):
                    st.image(
                        image, caption=f"Page {i+1}", use_column_width=True)

            sidebar.show_options()

            with chatbot_column:
                try:
                    history = ChatHistory()
                    chatbot = utils.setup_chatbot(
                        tmp_path, st.session_state["model"], st.session_state["temperature"]
                    )
                    st.session_state["chatbot"] = chatbot

                    if st.session_state["ready"]:
                        history.initialize(uploaded_file.name)

                        response_container, prompt_container = st.container(), st.container()

                        with prompt_container:
                            is_ready, user_input = layout.prompt_form()

                            if st.session_state["reset_chat"]:
                                history.reset()

                            if is_ready:
                                output = st.session_state["chatbot"].conversational_chat(
                                    user_input)

                        history.generate_messages(response_container)

                except Exception as e:
                    error_message = str(e)
                    stack_trace = traceback.format_exc()

                    st.error(
                        f"An error occurred: {error_message}\n{stack_trace}")
                    st.stop()

            sidebar.about()
