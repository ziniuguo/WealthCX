import csv
import requests
import pandas as pd
import mysql.connector

url = "https://dataapi.marketpsych.com/pulse/v4/equ/assets"
apiKey = "cus_YGeqOlvG3ca8GL"
outputFormat = "csv"

response = requests.get(url, params={"apikey": apiKey, "format": outputFormat})

if response.status_code == 200:
    # Save the CSV data to a file
    with open("asset.csv", "wb") as file:
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

# Load CSV data into a pandas DataFrame
df = pd.read_csv("asset.csv")

# Establish a MySQL connection and create a cursor

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# SQL commands
create_table_query = """
CREATE TABLE IF NOT EXISTS asset_mp (
    assetCode BIGINT PRIMARY KEY,
    name VARCHAR(255),
    RIC VARCHAR(255),
    version VARCHAR(255),
    filedate DATE,
    PermID BIGINT,
    TRBC BIGINT,
    TRBC_PermID BIGINT,
    TRBCEconomicSector VARCHAR(255),
    Ticker VARCHAR(255),
    MIC VARCHAR(255),
    Domicile VARCHAR(255),
    ExchangeCountry VARCHAR(255),
    ExchangeCode BIGINT,
    InfoCode BIGINT,
    Region VARCHAR(255),
    status VARCHAR(255)
)
"""

cursor.execute(create_table_query)
conn.commit()
cursor.close()
cursor = conn.cursor()

# Read the CSV file and insert data row by row
with open('asset.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        cursor.execute("""
                INSERT INTO asset_mp
                (assetCode, name, RIC, version, filedate, PermID, TRBC, TRBC_PermID, TRBCEconomicSector, 
                Ticker, MIC, Domicile, ExchangeCountry, ExchangeCode, InfoCode, Region, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, row)

# Commit the changes to the database


conn.commit()
cursor.close()
conn.close()

print("CSV data successfully imported into the MySQL table.")
