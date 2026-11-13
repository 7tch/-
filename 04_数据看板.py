import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()
speech_path = "data/speech_lib.csv"
comment_path = "data/comment_log.csv"

st.set_page_config(page_title="数据看板", layout="wide")
st.title("📊 直播数据看板")

tab1, tab2 = st.tabs(["话术统计", "评论统计"])

with tab1:
    st.subheader("话术库数据")
    if os.path.exists(speech_path):
        df_speech = pd.read_csv(speech_path)
        st.dataframe(df_speech, width="stretch")
        if not df_speech.empty:
            fig1 = px.histogram(df_speech, x="环节", title="各环节话术数量分布")
            st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("暂无话术数据，请先去话术生成器生成保存话术")

with tab2:
    st.subheader("评论互动数据")
    if os.path.exists(comment_path):
        df_comment = pd.read_csv(comment_path)
        st.dataframe(df_comment, width="stretch")
        if not df_comment.empty:
            fig2 = px.pie(df_comment, names="命中关键词", title="关键词命中占比")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("暂无评论数据，请先去评论机器人生成互动记录")
