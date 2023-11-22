import csv

import mysql.connector
import requests

url = "https://dataapi.marketpsych.com/pulse/v4/events/equ/hou/"
asset_code = "all"
apiKey = "cus_YGeqOlvG3ca8GL"
outputFormat = "csv"

response = requests.get(url + asset_code, params={"apikey": apiKey, "format": outputFormat})

if response.status_code == 200:
    # Save the CSV data to a file
    with open("event.csv", "wb") as file:
        file.write(response.content)
    print("CSV file downloaded successfully.")
else:
    print("Failed to download CSV file. Status code:", response.status_code)

# Define MySQL connection parameters
config = {
    "user": "doadmin",
    "password": "AVNS_tO45HWZ7rqlgDO7DoU-",
    "host": "db-mysql-sgp1-25924-do-user-14729808-0.b.db.ondigitalocean.com",
    "port": 25060,
    "database": "wealthcx",
}


# Establish a MySQL connection and create a cursor

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

drop = """DROP TABLE IF EXISTS event_mp"""
cursor.execute(drop)
conn.commit()
# SQL commands
create_table_query = """
CREATE TABLE IF NOT EXISTS event_mp (
    _id VARCHAR(255) PRIMARY KEY,
    Date DATETIME,
    assetClass VARCHAR(255),
    assetCode BIGINT,
    Headline VARCHAR(255),
    Topic VARCHAR(255),
    Sentiment VARCHAR(255),
    PulseLevel VARCHAR(255),
    Summary TEXT
)
"""

cursor.execute(create_table_query)
conn.commit()
cursor.close()
cursor = conn.cursor()

# Read the CSV file and insert data row by row
with open('event.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        row[1] = row[1].replace('T', ' ').replace('Z', '')
        cursor.execute("""
                INSERT INTO event_mp
                (_id, Date, assetClass, assetCode, Headline, Topic, Sentiment, PulseLevel, Summary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, row)

# Commit the changes to the database


conn.commit()
cursor.close()
conn.close()

print("CSV data successfully imported into the MySQL table.")
