import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from llm_api import ark_chat

load_dotenv()
csv_path = "data/comment_log.csv"

st.set_page_config(page_title="评论机器人", layout="wide")
st.title("💬 直播间评论机器人")

st.subheader("关键词库（命中关键词自动优先回复）")
keyword_text = st.text_area("一行一个关键词", value="多少钱\n包邮\n产地\n保质期")
keyword_list = [k.strip() for k in keyword_text.splitlines() if k.strip()]

st.subheader("模拟观众弹幕")
danmu = st.text_input("输入观众评论")

if st.button("生成回复", type="primary") and danmu:
    hit_key = None
    for kw in keyword_list:
        if kw in danmu:
            hit_key = kw
            break
    if hit_key:
        prompt = f"观众问：{danmu}，关键词：{hit_key}，你是农产品主播，简短口语回复。"
    else:
        prompt = f"观众弹幕：{danmu}，你是农产品主播，亲切简短回复。"

    res, err = ark_chat(prompt)
    if err:
        st.error(err)
    else:
        st.success("机器人回复：")
        st.write(res)
        # 保存记录
        new_row = pd.DataFrame([{
            "弹幕": danmu,
            "命中关键词": hit_key if hit_key else "无",
            "回复": res
        }])
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        st.info("✅ 记录已保存")

st.divider()
st.subheader("评论记录")
if os.path.exists(csv_path):
    df_show = pd.read_csv(csv_path)
    st.dataframe(df_show, width="stretch")
