import json
import streamlit as st

from utils import render_messages, create_chatbot


# ------------------------------网页------------------------------
page_title = "信息收集机器人（双agent）"
st.set_page_config(
    page_title=page_title,
    page_icon="🧾",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Hi! **Jamie** developed me! Contact him [here](https://github.com/dwjamie/chatbot) if you have any problems."
    },
)

# ------------------------------侧边栏------------------------------
with st.sidebar:
    st.header("机器人配置")
    chat_system_message = st.text_area(label="角色设定", placeholder="机器人需要扮演什么角色？")
    info_to_collect = st.text_area(label="信息收集", placeholder="有哪些需要向用户收集的信息？")
    model = st.selectbox("模型", options=["GPT-3.5", "GPT-4"])
    temperature = st.slider("随机性", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    change_config = st.button(label="更改配置")
    clean_history = st.button(label="清空对话历史")

form_system_message = f"""===
参考背景知识：
{chat_system_message}
===
需要扮演的角色：
本轮对话中，请扮演一个信息收集者，向用户收集信息。你将在谈话中不紧不慢地、一步步完善地询问和了解他们的信息。
如果用户的回答不符合要求或明显不合理，你将提醒他们重新回答。
如果你觉得他们的某个回答很不完整，或是有值得拓展之处，你将深入下去，多问几个问题，不断追问，直到你觉得清楚明白了为止。
最后，聊完以后，如果你确认收集全了所有的信息，请将你收集到的信息总结一遍告诉用户，待得到确认后，请调用submit_form函数提交信息表单。
===
需要向用户收集的信息:
{info_to_collect}"""


def apply_status():
    if "status" not in st.session_state or st.session_state.status == "chat":
        system_message = chat_system_message
        functions = [
            {
                "name": "start_form",
                "description": "Starts the process of filling out the form or collecting the needed information",
                "parameters": {"type": "object", "properties": {}},
            },
        ]
    elif st.session_state.status == "form":
        system_message = form_system_message
        functions = [
            {
                "name": "submit_form",
                "description": "Submits the completed information form",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collected_information": {
                            "type": "string",
                            "description": "All the collected information to be submitted on the form",
                        },
                    },
                    "required": ["collected_information"],
                },
            },
        ]
    return system_message, functions


system_message, functions = apply_status()

if "current_page" not in st.session_state:
    st.session_state.current_page = page_title

if st.session_state.current_page != page_title or "chatbot" not in st.session_state:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, functions, pl_tags=[page_title])
    st.session_state.current_page = page_title

if clean_history:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("对话历史已清空！", icon="✅")

if change_config:
    create_chatbot(model, temperature, system_message, functions, pl_tags=[page_title])
    st.info("机器人配置已更改！", icon="✅")

# ------------------------------对话框------------------------------
st.title(page_title)  # 渲染标题
render_messages(st.session_state.messages)  # 渲染对话历史
if user_message := st.chat_input("你好！"):
    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    call_function, assistant_message = st.session_state.chatbot.chat_no_stream(
        user_message, function_call=True
    )

    if call_function:
        parameters = json.loads(assistant_message["arguments"])
        with st.chat_message(name="assistant", avatar="🤖"):
            if assistant_message["name"] == "start_form":
                st.markdown("请点击以下按钮开始填写信息表单：")

                def start_button_on_click():
                    st.session_state.status = "form"
                    system_message, functions = apply_status()
                    create_chatbot(
                        model,
                        temperature,
                        system_message,
                        functions,
                        pl_tags=[page_title],
                    )
                    assistant_message = st.session_state.chatbot.chat_no_stream(
                        "", function_call=False
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                    )

                st.button(label="开始", on_click=start_button_on_click)
            elif assistant_message["name"] == "submit_form":
                st.markdown("请点击以下按钮开始提交信息表单：")

                def submit_button_on_click():
                    st.session_state.status = "chat"
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": f"表单已提交成功！信息如下：\n{parameters['collected_information']}",
                        }
                    )

                st.button(label="提交", on_click=submit_button_on_click)
    else:
        # 渲染并储存ChatBot消息
        with st.chat_message(name="assistant", avatar="🤖"):
            st.markdown(assistant_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )
