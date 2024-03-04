import streamlit as st
import agent


def create_chatbot(model, temperature, system_message, functions=None, pl_tags=[]):
    if model == "GPT-3.5 Turbo":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions,
            model="gpt-3.5-turbo",
            temperature=temperature,
            pl_tags=pl_tags,
        )
    elif model == "GPT-4 Turbo":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions,
            model="gpt-4-turbo-preview",
            temperature=temperature,
            pl_tags=pl_tags,
        )
    elif model == "Claude 2.1":
        st.session_state.chatbot = agent.Claude(
            model="claude-2.1", temperature=temperature, pl_tags=pl_tags
        )
    elif model == "Claude 3 Sonnet":
        st.session_state.chatbot = agent.Claude(
            model="claude-3-sonnet-20240229", temperature=temperature, pl_tags=pl_tags
        )
    elif model == "Claude 3 Opus":
        st.session_state.chatbot = agent.Claude(
            model="claude-3-opus-20240229", temperature=temperature, pl_tags=pl_tags
        )

    if system_message:
        st.session_state.chatbot.add_message(
            "system",
            system_message,
        )
    for message in st.session_state.messages:
        st.session_state.chatbot.add_message(message["role"], message["content"])
