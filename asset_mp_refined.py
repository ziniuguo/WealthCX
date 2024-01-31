import json

import mysql.connector

def asset_mp_refined():
    # Define MySQL connection parameters
    with open('./Configuration/database.config.json', 'r') as config_file:
        config = json.load(config_file)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS asset_mp_refined"""
    cursor.execute(drop)
    conn.commit()
    cursor.execute("""CREATE TABLE asset_mp_refined LIKE asset_mp""")
    cursor.execute("""INSERT INTO asset_mp_refined SELECT * FROM asset_mp WHERE RIC != ''""")

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
