import mysql.connector

config = {
        "user": "root",
        "password": "abc123",
        "host": "localhost",
        "port": 3306,
        "database": "wealthcx",
    }

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
