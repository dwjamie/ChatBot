import streamlit as st
import os

import promptlayer

promptlayer.api_key = st.secrets["promptlayer"]["api_key"]

openai = promptlayer.openai
openai.api_key = st.secrets["openai"]["api_key"]

anthropic = promptlayer.anthropic
os.environ["ANTHROPIC_API_KEY"] = st.secrets["anthropic"]["api_key"]


class OpenAI:
    def __init__(self, **kwargs):
        self.messages = kwargs.get("messages", [])
        self.functions = kwargs.get("functions", None)
        self.model = kwargs.get("model", "gpt-3.5-turbo")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def chat_no_stream(self, user_message, function_call=False):
        self.messages.append({"role": "user", "content": user_message})
        if not function_call:
            assistant_message = openai.ChatCompletion.create(
                messages=self.messages,
                model=self.model,
                temperature=self.temperature,
                pl_tags=self.pl_tags,
            )["choices"][0]["message"]
            self.messages.append(assistant_message)
            return assistant_message["content"]
        else:
            assistant_message = openai.ChatCompletion.create(
                messages=self.messages,
                functions=self.functions,
                model=self.model,
                temperature=self.temperature,
                pl_tags=self.pl_tags,
            )["choices"][0]["message"]
            if assistant_message["content"]:
                self.messages.append(assistant_message)
                return False, assistant_message["content"]
            else:
                return True, assistant_message["function_call"]

    def chat(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        assistant_response = openai.ChatCompletion.create(
            messages=self.messages,
            model=self.model,
            temperature=self.temperature,
            stream=True,
            pl_tags=self.pl_tags,
        )
        for chunk in assistant_response:
            chunk = chunk["choices"][0]["delta"]
            if chunk.get("content"):
                yield chunk["content"]


class Claude:
    def __init__(self, **kwargs):
        anthropic.api_key = st.secrets["anthropic"]["api_key"]
        self.messages = kwargs.get("messages", "")
        self.model = kwargs.get("model", "claude-2.1")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        if role == "assistant":
            self.messages += "\n\nAssistant:" + " " + content
        else:
            self.messages += "\n\nHuman:" + " " + content

    def chat_no_stream(self, user_message):
        self.messages += "\n\nHuman:" + " " + user_message + "\n\nAssistant:" + " "
        claude = anthropic.Anthropic()
        assistant_message = claude.completions.create(
            prompt=self.messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens_to_sample=2048,
            pl_tags=self.pl_tags,
        ).completion
        self.messages += assistant_message
        return assistant_message

    def chat(self, user_message):
        self.messages += "\n\nHuman:" + " " + user_message + "\n\nAssistant:" + " "
        claude = anthropic.Anthropic()
        assistant_response = claude.completions.create(
            prompt=self.messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens_to_sample=2048,
            stream=True,
            pl_tags=self.pl_tags,
        )
        for chunk in assistant_response:
            yield chunk.completion
