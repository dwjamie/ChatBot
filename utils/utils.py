import streamlit as st


def render_messages(messages):
    for message in messages:
        if message["role"] == "user":
            avatar = "🧑‍💻"
        elif message["role"] == "assistant":
            avatar = "🤖"
        elif message["role"] == "system":
            avatar = "🔧"
        with st.chat_message(name=message["role"], avatar=avatar):
            st.markdown(message["content"])
