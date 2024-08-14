import json
import jpy_datareader as jdr
import pandas as pd
import streamlit as st

# 環境変数の読み込み
with open('env.json', 'r') as f:
    env_vars = json.load(f)

api_key = env_vars['API_KEY']
df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003293502")

# ユニークなテスト項目のリスト
df_test_items_unique = df['体格測定・テスト項目'].unique()

# ドロップダウンメニューとして表示
selected_test_item = st.selectbox(
    '体格測定・テスト項目を選択してください',
    df_test_items_unique
)

# 選択された項目を表示
st.write('選択された項目:', selected_test_item)

# 選択した項目に基づいてフィルタリング
df_filtered = df[
    (df['性別'] == '女子') &
    (df['体格測定・テスト項目'] == selected_test_item)
]

df_grouped = df_filtered.groupby(['運動部・スポーツクラブ所属', '時間軸(年度次)'])['平均値'].mean().unstack()

# 棒グラフの作成
import matplotlib.pyplot as plt
import japanize_matplotlib

fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.4
years = df_grouped.columns
r1 = range(len(years))
r2 = [x + bar_width for x in r1]

bars1 = ax.bar(r1, df_grouped.loc['所属していない'], color='skyblue', width=bar_width, edgecolor='grey', label='所属していない')
bars2 = ax.bar(r2, df_grouped.loc['所属している'], color='salmon', width=bar_width, edgecolor='grey', label='所属している')

ax.set_xlabel('年度')
ax.set_ylabel('平均値')
ax.set_title(f'{selected_test_item} 年度別: 所属している vs 所属していない')
ax.set_xticks([x + bar_width / 2 for x in r1])
ax.set_xticklabels(years)
ax.legend()

# グラフの表示
st.pyplot(fig)

# 散布図を折れ線グラフに変更する
df_scatter = df_filtered.groupby('運動テスト年齢')['平均値'].mean().reset_index()

# Streamlitで折れ線グラフを表示
st.line_chart(df_scatter.set_index('運動テスト年齢')['平均値'])
