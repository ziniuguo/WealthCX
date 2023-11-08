import mysql.connector
import pandas as pd

import refinitiv_price

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
