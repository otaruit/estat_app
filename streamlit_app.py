import streamlit as st
import numpy as np
import pandas as pd
import main

st.title('Streamlit 基本操作')

st.write('Streamlit 練習')

df = pd.DataFrame({
    '1列目': [1, 2, 3, 4],
    '2列目': [10, 20, 30, 40],
})

st.dataframe(df.style.highlight_max(axis=0))

# # 表示
# st.write(df)

df = pd.DataFrame(
    # 行20 列3で乱数を生成
    np.random.rand(20, 3),
    # カラム名
    columns=['a', 'b', 'c']
)

st.line_chart(df)

st.area_chart(df)

df = pd.DataFrame(
    # 新宿付近
    np.random.rand(100, 2)/[50, 50]  + [43.19, 140.99],
    # latitude 緯度 longitude 経度
    columns=['lat', 'lon']
)

st.map(df)

