# Import standard libraries
import os
import traceback

# Import third-party libraries
import streamlit as st

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
        os.environ["OPEN_API_KEY"] = user_api_key
        pdf = utils.handle_upload()

        if pdf:
            sidebar.show_options()

            try:
                history = ChatHistory()
                chatbot = utils.setup_chatbot(
                    pdf, st.session_state["model"], st.session_state["temperature"]
                )
                st.session_state["chatbot"] = chatbot

                if st.session_state["ready"]:
                    history.initialize(pdf.name)

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

                st.error(f"An error occurred: {error_message}\n{stack_trace}")
                # st.stop()

    sidebar.about()
