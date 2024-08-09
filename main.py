import json
import jpy_datareader as jdr


# env.json ファイルを読み込む
with open('env.json', 'r') as f:
    env_vars = json.load(f)

# API_KEY を取得する
api_key = env_vars['API_KEY']
df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003000795")
print(df)