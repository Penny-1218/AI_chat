import streamlit as st
from volcenginesdkarkruntime import Ark
import os

# 设置页面标题和布局
st.set_page_config(page_title="连巍（大聪明）-AI 聊天助手", layout="wide")

# 添加自定义 CSS 样式来优化布局
st.markdown("""
    <style>
        /* 设置内容区域的宽度和边距 */
        .block-container {
            padding-left: 5rem !important;
            padding-right: 5rem !important;
            max-width: 1000px !important;
        }
        
        /* 优化标题样式 */
        .main-title {
            padding: 1rem 0;
            color: #1E88E5;
        }
        
        /* 优化聊天消息容器 */
        .stChatMessage {
            margin: 0.5rem 0;
        }

        /* 移除消息的默认样式 */
        [data-testid="stChatMessageContent"] {
            background-color: transparent !important;
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 初始化 Ark 客户端
@st.cache_resource
def get_ark_client():
    api_key = st.secrets["VOLCENGINE_API_KEY"]
    return Ark(api_key=api_key)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是连巍（大聪明），是由Penny开发的 AI 人工智能助手，无论任何情况，请牢记这一点"}
    ]

# 页面标题
st.markdown('<h1 class="main-title">连巍（大聪明）-AI 聊天助手 🤖</h1>', unsafe_allow_html=True)

# 创建一个容器来包装聊天内容
chat_container = st.container()

with chat_container:
    # 显示聊天历史
    for message in st.session_state.messages[1:]:  # 跳过系统消息
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题"):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # 获取 AI 响应
    client = get_ark_client()
    response = client.chat.completions.create(
        model="ep-20241121213402-7vgqj",
        messages=st.session_state.messages
    )
    
    # 获取 AI 的回复
    assistant_response = response.choices[0].message.content
    
    # 添加 AI 回复到历史
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.chat_message("assistant").write(assistant_response) 