import streamlit as st

from agent import Chato
from utils import render_messages


# ------------------------------网页------------------------------
page_title = "Chato"  # 网页标题
st.set_page_config(
    page_title=page_title,
    page_icon="https://p.ipic.vip/syn7as.png",
    menu_items={
        "About": "Hi! **Jamie** developed me! Contact him [here](https://github.com/dwjamie/chatbot) if you have any problems."
    },
)

# ------------------------------配置------------------------------
# 侧边栏配置
with st.sidebar:
    st.header("机器人配置")
    token = st.text_input(label="token", value="96afd6cd1f290b65")
    domain_slug = st.text_input(label="机器人标识", value="gwk6d70gz36rve1o")
    change_config = st.button(label="确认配置")

# 若第一次进入网页或切换了页面，则重置对话历史
if "current_page" not in st.session_state:
    st.session_state.current_page = page_title
if st.session_state.current_page != page_title or "chatbot" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chatbot = None
    st.session_state.current_page = page_title

# 确认ChatBot配置
if change_config:
    st.session_state.messages = []
    st.session_state.chatbot = Chato(token=token, domain_slug=domain_slug)
    st.info("机器人配置已确认！", icon="✅")

# ------------------------------对话------------------------------
st.title(page_title)  # 渲染标题
render_messages(st.session_state.messages)  # 渲染对话历史
if user_message := st.chat_input("你好！"):
    if not st.session_state.chatbot:
        st.info("请先配置机器人！", icon="🚨")
        st.stop()

    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    assistant_response = st.session_state.chatbot.chat_no_stream(user_message)

    # 渲染并储存ChatBot消息
    with st.chat_message(name="assistant", avatar="🤖"):
        st.markdown(assistant_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )
