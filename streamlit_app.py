import jpy_datareader as jdr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st
import json



# font_path = 'fonts/ipag.ttf'
# font_prop = font_manager.FontProperties(fname=font_path)

# plt.rcParams['font.family'] = font_prop.get_name()


api_key = st.secrets["API_KEY"]
df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003293502")

df_test_items_unique = df['体格測定・テスト項目'].unique()
selected_test_item = st.selectbox('体格測定・テスト項目を選択してください', df_test_items_unique)

comparison_item = st.selectbox('比較する項目を選択してください', ['性別', '運動部・スポーツクラブ所属'])

age_options = df['運動テスト年齢'].unique().tolist() 
age_options.append('全年齢の平均')  
age_selection = st.selectbox('年齢を選択してください', age_options)

df_filtered = df[df['体格測定・テスト項目'] == selected_test_item]

if age_selection == '全年齢の平均':
    df_grouped = df_filtered.groupby([comparison_item, '時間軸(年度次)'])['平均値'].mean().unstack()
    title_suffix = '全年齢平均'
else:
    df_filtered = df_filtered[df_filtered['運動テスト年齢'] == age_selection]
    df_grouped = df_filtered.groupby([comparison_item, '時間軸(年度次)'])['平均値'].mean().unstack()
    title_suffix = f'{age_selection} 別'

if df_grouped.empty:
    st.write("データがありません。条件を変更して再試行してください。")
else:
    fig, ax = plt.subplots(figsize=(12, 6))

    df_grouped.T.plot(ax=ax, marker='o')

    ax.set_xlabel('年度')
    ax.set_ylabel('平均値')
    ax.set_title(f'{selected_test_item} の {comparison_item} 別平均値 ({title_suffix})')
    ax.legend(title=comparison_item)

    st.pyplot(fig)
