import streamlit as st
import os

import promptlayer

promptlayer.api_key = st.secrets["promptlayer"]["api_key"]

openai = promptlayer.openai
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]

anthropic = promptlayer.anthropic
os.environ["ANTHROPIC_API_KEY"] = st.secrets["anthropic"]["api_key"]


class OpenAI:
    def __init__(self, **kwargs):
        self.messages = kwargs.get("messages", [])
        self.model = kwargs.get("model", "gpt-3.5-turbo")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def chat_no_stream(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        chatgpt = openai.OpenAI()
        assistant_message = (
            chatgpt.chat.completions.create(
                messages=self.messages,
                model=self.model,
                temperature=self.temperature,
                pl_tags=self.pl_tags,
            )
            .choices[0]
            .message
        )
        return assistant_message.content

    def chat(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        chatgpt = openai.OpenAI()
        assistant_response = chatgpt.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=self.temperature,
            stream=True,
            pl_tags=self.pl_tags,
        )
        for chunk in assistant_response:
            token = chunk.choices[0].delta
            if token.content:
                yield token.content


class Claude:
    def __init__(self, **kwargs):
        anthropic.api_key = st.secrets["anthropic"]["api_key"]
        self.messages = kwargs.get("messages", [])
        self.system = ""
        self.model = kwargs.get("model", "claude-2.1")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        if role in ["user", "assistant"]:
            if len(self.messages) >= 1 and self.messages[-1]["role"] == role:
                self.messages[-1]["content"] += "\n" + content
            else:
                self.messages.append({"role": role, "content": content})
        elif role == "system":
            self.system = content

    def chat_no_stream(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        claude = anthropic.Anthropic()
        assistant_message = (
            claude.messages.create(
                messages=self.messages,
                system=self.system,
                model=self.model,
                temperature=self.temperature,
                max_tokens=2048,
                pl_tags=self.pl_tags,
            )
            .content[0]
            .text
        )
        return assistant_message

    def chat(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        claude = anthropic.Anthropic()
        with claude.messages.stream(
            messages=self.messages,
            system=self.system,
            model=self.model,
            temperature=self.temperature,
            max_tokens=2048,
            pl_tags=self.pl_tags,
        ) as assistant_response:
            for token in assistant_response.text_stream:
                if token:
                    yield token
