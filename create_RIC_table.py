import mysql.connector

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

# Query to create a new table 'asset_mp_refined' excluding rows where RIC is empty
# Create a new table 'asset_mp_refined' with the same structure as 'asset_mp'
cursor.execute("""CREATE TABLE asset_mp_refined LIKE asset_mp""")

# Insert rows from 'asset_mp' excluding rows where RIC is empty
cursor.execute("""INSERT INTO asset_mp_refined SELECT * FROM asset_mp WHERE RIC != ''""")

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
