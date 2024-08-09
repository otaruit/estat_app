

import jpy_datareader as jdr
api_key = "105b557649ea929878fe7f927b520fcfa202ccee"

df = jdr.get_data_estat_statsdata(api_key, statsDataId="0003000795")
print(df)