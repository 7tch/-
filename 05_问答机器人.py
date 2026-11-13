import streamlit as st
from dotenv import load_dotenv
from llm_api import ark_chat

load_dotenv()

st.set_page_config(page_title="问答机器人", layout="wide")
st.title("🙋 农产品问答助手")
st.info("用来解答产品相关疑问，回答通俗易懂，适合直播间参考")

user_q = st.text_input("请输入问题：")

if st.button("获取回答", type="primary") and user_q.strip():
    prompt = f"""
你是农产品直播间的答疑主播，回答简短朴实，通俗易懂。
观众提问：{user_q}
"""
    res, err = ark_chat(prompt)
    if err:
        st.error(f"❌ 出错：{err}")
    else:
        st.success("✅ 回答：")
        st.write(res)
