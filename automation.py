import mysql.connector
import pandas as pd

import refinitiv_price
import hawkeye_signal
import json

ric_value = "AAPL.O"

config = {
    "user": "doadmin",
    "password": "AVNS_tO45HWZ7rqlgDO7DoU-",
    "host": "db-mysql-sgp1-25924-do-user-14729808-0.b.db.ondigitalocean.com",
    "port": 25060,
    "database": "wealthcx",
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# get one day of refinitiv, populate to db
refinitiv_price.populate(ric_value)
# get assetCode by RIC
query = "SELECT asset_mp_refined.assetCode FROM asset_mp_refined WHERE RIC = %s"
cursor.execute(query, (ric_value,))
assetCode = cursor.fetchone()
assetCode = assetCode[0]

# Join refinitiv, event (both only latest) and asset
sql_query = f"""
SELECT * FROM asset_mp_refined 
INNER JOIN event_mp ON event_mp.assetCode = '{assetCode}' AND asset_mp_refined.assetCode = '{assetCode}' AND Sentiment != '' 
INNER JOIN refinitiv
ORDER BY event_mp.Date DESC LIMIT 1
"""

print(sql_query)


df = pd.read_sql(sql_query, conn)

df = df.drop(columns=['Idx'], errors='ignore')

cols = pd.Series(df.columns)
for dup in cols[cols.duplicated()].unique():
    cols[df.columns.get_loc(dup)] = [f'{dup}_{i}' if i != 0 else dup for i in range(df.columns.get_loc(dup).sum())]
df.columns = cols
df = df.drop(columns=['assetCode_1'], errors='ignore')

csv_file = 'output.csv'
df.to_csv(csv_file, index=False)

conn.close()

# Let's assume 'original_table' is your DataFrame from the existing table.
# And 'json_data' is a dictionary containing the parsed JSON data.

# Convert the original table into a DataFrame if it's not already.
original_table = df  # replace 'original_table_data' with your actual data variable

with open('hawkeye.json', 'r') as json_file:
    # 使用json.load()方法加载JSON文件内容
    json_data_with_single_quotes = json_file.read()

# 将单引号替换为双引号
json_data_with_double_quotes = json_data_with_single_quotes.replace("'", "\"")

# 解析转换后的JSON数据
json_data = json.loads(json_data_with_double_quotes)


# json_data = hawkeye_signal.get_hawkeye_data()
# Extract the relevant data from the JSON.
json_extracted_data = {
    "ticker_currency": json_data['AAPL.O']['ticker_currency'],
    "algo_short_description": json_data['AAPL.O']['algo_short_description'],
    "number_events": json_data['AAPL.O']['number_events'],
    "event_period_units": json_data['AAPL.O']['event_period_units'],
    "outlook_period": json_data['AAPL.O']['outlook_period'],
    "outlook_period_length": json_data['AAPL.O']['outlook_period_length'],
    "event_signal_date": json_data['AAPL.O']['event_signal_date'],
    "ticker_last_close_price": json_data['AAPL.O']['ticker_last_close_price'],
    "optimal_period": json_data['AAPL.O']['optimal_period'],
    "data_analyzed_from": json_data['AAPL.O']['data_analyzed_from'],
    "expected_average_return": json_data['AAPL.O']['expected_average_return'],
    "expected_win_rate": json_data['AAPL.O']['expected_win_rate'],
    # Assuming event_abs_instances is a list of dictionaries
    "event_abs_instances": [instance['trade_returns'] for instance in json_data['AAPL.O']['event_abs_instances']],
    "event_abs_stats": json_data['AAPL.O']['event_abs_stats']
}

# Create a DataFrame from the extracted JSON data.
json_df = pd.DataFrame([json_extracted_data])

# Merge the JSON data with the original table.
# This assumes that the JSON data and the original table are aligned by index.
# If they are not, you will need to find a common key to merge on.
merged_table = pd.concat([original_table, json_df], axis=1)

# Now export the merged table to a CSV file.
merged_table.to_csv('merged_table.csv', index=False)