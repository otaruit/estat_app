import json
import jpy_datareader as jdr
import pandas as pd
import streamlit as st

# env.json ファイルを読み込む
with open('env.json', 'r') as f:
    env_vars = json.load(f)

# API_KEY を取得する
api_key = env_vars['API_KEY']
df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003293502")


# データフレームの先頭を表示
# print(df)


# データのフィルタリング
df_filtered = df[(df['性別'] == '女子') &  (df['体格測定・テスト項目'] == 'テスト_10m障害物歩行（秒）')]

print(df_filtered)

# # データの整形
# df_grouped = df.groupby(["性別", "身長"])["出生数"].sum().reset_index()

# # 性別ごとにデータを分けて円グラフを表示
# for gender in df_grouped["性別"].unique():
#     df_gender = df_grouped[df_grouped["性別"] == gender]
    
#     st.subheader(f"{gender}の身長別出生数")
#     st.write(df_gender)  # データを表示（オプション）

#     # 円グラフの作成
#     st.pyplot(df_gender.set_index("身長")["出生数"].plot(kind='pie', autopct='%1.1f%%', title=f"{gender}の身長別出生数").get_figure())
