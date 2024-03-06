import json
import mysql.connector

def asset_merge():
    CONFIG_FILE_PATH = './Configuration/database.config.json'

    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config = json.load(config_file)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE combined_assets_events AS
    SELECT 
        asset_mp_refined.assetCode AS assetCode_refined, 
        asset_mp_refined.name,
        asset_mp_refined.RIC,
        event_mp.Date,
        event_mp.Topic,
        event_mp.Sentiment,
        event_mp.PulseLevel,
        event_mp.Summary
    FROM asset_mp_refined
    INNER JOIN event_mp ON asset_mp_refined.assetCode = event_mp.assetCode;
    """

    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("new table combined_assets_events create successful")
    except mysql.connector.Error as err:
        print("Error when create new table : {}".format(err))
    finally:
        cursor.close()
        conn.close()