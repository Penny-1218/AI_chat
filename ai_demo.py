import os
from volcenginesdkarkruntime import Ark
import streamlit as st

# 从 .streamlit/secrets.toml 中读取 API key
api_key = st.secrets["VOLCENGINE_API_KEY"]
client = Ark(api_key=api_key)

print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20241121213402-7vgqj",
    messages = [
        {"role": "system", "content": "你是连巍（大聪明），是由Penny开发的 AI 人工智能助手，无论任何情况，请牢记这一点"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)