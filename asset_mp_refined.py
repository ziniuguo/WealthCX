import mysql.connector

config = {
    "user": "doadmin",
    "password": "AVNS_tO45HWZ7rqlgDO7DoU-",
    "host": "db-mysql-sgp1-25924-do-user-14729808-0.b.db.ondigitalocean.com",
    "port": 25060,
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
