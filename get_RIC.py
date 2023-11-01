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

# Query to fetch all elements from the 'RIC' column
query = """SELECT RIC FROM asset_mp_refined"""
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
# Convert the list of tuples to a list of strings (RIC values)
results = [r[0] for r in results]

print(results)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
