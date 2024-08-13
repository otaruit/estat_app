import json
import jpy_datareader as jdr
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib # 追加



with open('env.json', 'r') as f:
    env_vars = json.load(f)


api_key = env_vars['API_KEY']
df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003293502")

print(df)


df_filtered = df[
    (df['性別'] == '女子') &
    (df['体格測定・テスト項目'] == 'テスト_10m障害物歩行（秒）')
]


df_grouped = df_filtered.groupby(['運動部・スポーツクラブ所属', '時間軸(年度次)'])['平均値'].mean().unstack()


st.title('運動部・スポーツクラブ所属別のテスト結果')


fig, ax = plt.subplots(figsize=(12, 6))


bar_width = 0.4

years = df_grouped.columns

r1 = range(len(years))
r2 = [x + bar_width for x in r1]


bars1 = ax.bar(r1, df_grouped.loc['所属していない'], color='skyblue', width=bar_width, edgecolor='grey', label='所属していない')
bars2 = ax.bar(r2, df_grouped.loc['所属している'], color='salmon', width=bar_width, edgecolor='grey', label='所属している')


ax.set_xlabel('年度')
ax.set_ylabel('平均値')
ax.set_title('テスト_10m障害物歩行（秒） 年度別: 所属している vs 所属していない')
ax.set_xticks([x + bar_width / 2 for x in r1])
ax.set_xticklabels(years)
ax.legend()


ax.set_ylim(6.5, 8)


st.pyplot(fig)
