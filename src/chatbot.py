# Import third-party libraries
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from typing import Any


class Chatbot:
    """Class for managing chatbot interactions."""

    def __init__(self, model_name: str, temperature: float, vectors: Any):
        """Initializes the chatbot with a model, temperature, and document vectors.

        Args:
            model_name (str): The name of the model to be used.
            temperature (float): The temperature setting for the model's responses.
            vectors (Any): The document vectors for the retrieval of responses.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    def conversational_chat(self, query: str) -> str:
        """Starts a conversational chat with a model via Langchain.

        Args:
            query (str): The query to be passed to the model.

        Returns:
            str: The model's response.
        """
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.model_name,
                           temperature=self.temperature),
            memory=st.session_state["history"],
            retriever=self.vectors.as_retriever(),
        )
        result = chain({"question": query})

        return result["answer"]
