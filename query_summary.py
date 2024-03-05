import json
import mysql.connector

CONFIG_FILE_PATH = './Configuration/database.config.json'

def query_combined_table(ric):
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config = json.load(config_file)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
        RIC, 
        Date, 
        Topic, 
        Sentiment, 
        PulseLevel, 
        Summary
    FROM combined_assets_events
    WHERE RIC = %s
    ORDER BY Date DESC
    LIMIT 5;
    """

    try:
        cursor.execute(query, (ric,))
        results = cursor.fetchall()
        return json.dumps(results, default=str)
    except mysql.connector.Error as err:
        print("查询数据时出错: {}".format(err))
        return json.dumps({'error': str(err)})
    finally:
        cursor.close()
        conn.close()

ric_to_query = 'JPM'
json_result = query_combined_table(ric_to_query)
print(json_result)