import csv
import json
import os

import requests
import mysql.connector

def asset_mp():
    url = "https://dataapi.marketpsych.com/pulse/v4/equ/assets"
    apiKey = "cus_YGeqOlvG3ca8GL"
    outputFormat = "csv"

    response = requests.get(url, params={"apikey": apiKey, "format": outputFormat})

    if response.status_code == 200:
        # 保存CSV数据到Output文件夹下的asset.csv
        output_folder = "./Output"
        os.makedirs(output_folder, exist_ok=True)  # 确保Output文件夹存在
        asset_file_path = os.path.join(output_folder, "asset.csv")

        with open(asset_file_path, "wb") as file:
            file.write(response.content)
        print("CSV file downloaded successfully.")
    else:
        print("Failed to download CSV file. Status code:", response.status_code)

    # Define MySQL connection parameters
    with open('./Configuration/database.config.json', 'r') as config_file:
        config = json.load(config_file)

    # Establish a MySQL connection and create a cursor

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS asset_mp"""
    cursor.execute(drop)
    conn.commit()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS asset_mp (
        assetCode BIGINT PRIMARY KEY,
        name VARCHAR(255),
        RIC VARCHAR(255),
        filedate DATE,
        TRBC BIGINT,
        TRBCEconomicSector VARCHAR(255),
        Ticker VARCHAR(255),
        MIC VARCHAR(255),
        Domicile VARCHAR(255),
        ExchangeCountry VARCHAR(255),
        Region VARCHAR(255),
        status VARCHAR(255)
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    cursor = conn.cursor()

    # Read the CSV file and insert data row by row
    with open(asset_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            # Replace empty strings with None (NULL)
            row = [None if x == '' else x for x in row]
            cursor.execute("""
                INSERT INTO asset_mp
                (assetCode, name, RIC, filedate, TRBC, TRBCEconomicSector, Ticker, MIC, Domicile, ExchangeCountry, Region, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, row)

    # Commit the changes to the database


    conn.commit()
    cursor.close()
    conn.close()

    print("CSV data successfully imported into the MySQL table.")

# asset_mp()