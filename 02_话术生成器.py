import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from llm_api import ark_chat

load_dotenv()
csv_path = "data/speech_lib.csv"

st.set_page_config(page_title="话术生成器", layout="wide")
st.title("🎤 直播话术生成器")

product = st.text_input("产品名称")
sell_point = st.text_area("核心卖点")
scene = st.selectbox("直播环节", ["开场介绍","讲解产品","促单逼单","回复疑问","收尾"])

if st.button("生成话术", type="primary"):
    prompt = f"""
你是农产品直播主播，口语简短接地气。
产品：{product}
卖点：{sell_point}
环节：{scene}
直接输出话术，不要多余解释。
"""
    res, err = ark_chat(prompt)
    if err:
        st.error(err)
    else:
        st.success("生成结果：")
        st.write(res)
        # 保存到csv
        new_row = pd.DataFrame([{"产品":product,"卖点":sell_point,"环节":scene,"话术":res}])
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        st.info("✅ 话术已保存到 data/speech_lib.csv")

st.divider()
st.subheader("历史话术库")
if os.path.exists(csv_path):
    df_show = pd.read_csv(csv_path)
    st.dataframe(df_show, width="stretch")
