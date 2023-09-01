import streamlit as st

import json
import requests

import promptlayer

promptlayer.api_key = st.secrets["promptlayer"]["api_key"]
openai = promptlayer.openai
anthropic = promptlayer.anthropic


class OpenAI:
    def __init__(self, **kwargs):
        openai.api_type = "open_ai"
        openai.api_version = None
        openai.api_base = st.secrets["openai"]["api_base"]
        openai.api_key = st.secrets["openai"]["api_key"]
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


class AzureOpenAI:
    def __init__(self, **kwargs):
        openai.api_type = "azure"
        openai.api_version = "2023-03-15-preview"  # "2023-05-15"
        openai.api_base = st.secrets["azure"]["api_base"]
        openai.api_key = st.secrets["azure"]["api_key"]
        self.messages = kwargs.get("messages", [])
        self.functions = kwargs.get("functions", None)
        self.engine = kwargs.get("model", "gpt-35-turbo")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def chat_no_stream(self, user_message, function_call=False):
        self.messages.append({"role": "user", "content": user_message})
        if not function_call:
            assistant_message = openai.ChatCompletion.create(
                messages=self.messages,
                engine=self.engine,
                temperature=self.temperature,
                pl_tags=self.pl_tags,
            )["choices"][0]["message"]
            self.messages.append(assistant_message)
            return assistant_message["content"]
        else:
            assistant_message = openai.ChatCompletion.create(
                messages=self.messages,
                functions=self.functions,
                engine=self.engine,
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
            engine=self.engine,
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
        self.model = kwargs.get("model", "claude-2")
        self.temperature = kwargs.get("temperature", None)
        self.pl_tags = kwargs.get("pl_tags", [])

    def add_message(self, role, content):
        if role == "assistant":
            self.messages += anthropic.AI_PROMPT + " " + content
        else:
            self.messages += anthropic.HUMAN_PROMPT + " " + content

    def chat_no_stream(self, user_message):
        self.messages += (
            anthropic.HUMAN_PROMPT + " " + user_message + anthropic.AI_PROMPT + " "
        )
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
        self.messages += (
            anthropic.HUMAN_PROMPT + " " + user_message + anthropic.AI_PROMPT + " "
        )
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


class Chato:
    def __init__(self, **kwargs):
        self.token = kwargs.get("token", "")
        self.domain_slug = kwargs.get("domain_slug", "")

    def chat_no_stream(self, user_message):
        url = f"http://api.chato.cn/chato/api-public/domains/{self.domain_slug}/chat"
        payload = json.dumps({"p": user_message, "uid": "123", "token": "1111"})
        headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload).text
        response = json.loads(response)
        return response["data"]["content"]

    def chat(self, user_message):
        url = f"http://api.chato.cn/sse/{self.domain_slug}"
        payload = json.dumps({"p": user_message, "token": self.token})
        headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        for chunk in response:
            yield chunk  # 暂时有bug
