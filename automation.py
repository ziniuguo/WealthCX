import csv
import os

import mysql.connector
import pandas as pd

import refinitiv_price
import json

def check_file_existence(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False
    return True

def automate(uuid, ric_value):
    # Define MySQL connection parameters
    with open('./Configuration/database.config.json', 'r') as config_file:
        config = json.load(config_file)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # get one day of refinitiv, populate to db
    refinitiv_price.populate(uuid, ric_value)
    # get assetCode by RIC
    query = "SELECT asset_mp_refined.assetCode FROM asset_mp_refined WHERE RIC = %s"
    cursor.execute(query, (ric_value,))
    asset_code = cursor.fetchone()
    asset_code = asset_code[0]

    # Join event and asset
    sql_query = f"""
    SELECT * FROM asset_mp_refined 
    INNER JOIN event_mp ON event_mp.assetCode = '{asset_code}' AND asset_mp_refined.assetCode = '{asset_code}' AND Sentiment != '' 
    ORDER BY event_mp.Date DESC LIMIT 1
    """

    df = pd.read_sql(sql_query, conn)

    conn.close()

    df = df.drop(columns=['Idx'], errors='ignore')

    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[df.columns.get_loc(dup)] = [f'{dup}_{i}' if i != 0 else dup for i in range(df.columns.get_loc(dup).sum())]
    df.columns = cols
    df = df.drop(columns=['assetCode_1'], errors='ignore')

    original_table = df  # replace 'original_table_data' with your actual data variable

    # 使用open函数和json.load方法读取和解析JSON文件
    with open('./Output/HawkeyeData.json', 'r') as json_file:
        json_data = json.load(json_file)

    # 根据JSON文件的结构提取数据
    # 这里的代码可能需要根据您的实际JSON文件结构进行调整
    # Extract the relevant data from the JSON.
    json_extracted_data = {
        "ticker_currency": json_data[ric_value]['ticker_currency'],
        "algo_short_description": json_data[ric_value]['algo_short_description'],
        "number_events": json_data[ric_value]['number_events'],
        "event_period_units": json_data[ric_value]['event_period_units'],
        "outlook_period": json_data[ric_value]['outlook_period'],
        "outlook_period_length": json_data[ric_value]['outlook_period_length'],
        "event_signal_date": json_data[ric_value]['event_signal_date'],
        "ticker_last_close_price": json_data[ric_value]['ticker_last_close_price'],
        "optimal_period": json_data[ric_value]['optimal_period'],
        "data_analyzed_from": json_data[ric_value]['data_analyzed_from'],
        "expected_average_return": json_data[ric_value]['expected_average_return'],
        "expected_win_rate": json_data[ric_value]['expected_win_rate'],
        # Assuming event_abs_instances is a list of dictionaries
        "event_abs_instances": [instance['trade_returns'] for instance in json_data[ric_value]['event_abs_instances']],
        "event_abs_stats": json_data[ric_value]['event_abs_stats']
    }

    # Create a DataFrame from the extracted JSON data.
    json_df = pd.DataFrame([json_extracted_data])

    # Merge the JSON data with the original table.
    # This assumes that the JSON data and the original table are aligned by index.
    # If they are not, you will need to find a common key to merge on.
    merged_table = pd.concat([original_table, json_df], axis=1)

    # Now export the merged table to a CSV file.
    temp_csv_path = f'./Output/{uuid}-temp.csv'
    merged_table.to_csv(temp_csv_path, index=False)

    # 读取和合并CSV文件的路径也应该更新
    csv_file1 = temp_csv_path
    csv_file2 = f'./Output/{uuid}-refinitiv.csv'
    output_csv = f'./Output/{uuid}-output.csv'

    # Read the header and the first data line from each CSV file
    with open(csv_file1, 'r') as file1, open(csv_file2, 'r') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        header1 = next(reader1, None)  # Read header from the first file
        header2 = next(reader2, None)  # Read header from the second file

        line1 = next(reader1, None)  # Read first data line from the first file
        line2 = next(reader2, None)  # Read first data line from the second file

    # Combine the headers and the data lines
    combined_header = header1 + header2 if header1 and header2 else None
    combined_line = line1 + line2 if line1 and line2 else None

    # Write the combined header and data line to a new CSV file
    if combined_header and combined_line:
        with open(output_csv, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(combined_header)
            writer.writerow(combined_line)
        print(f"Combined CSV with header written to {output_csv}")
    else:
        print("One of the files is empty, missing, or does not contain data beyond the header.")

    # 合并完成后，删除生成的临时CSV文件
    if os.path.exists(temp_csv_path):
        os.remove(temp_csv_path)
        print(f"Temporary CSV file {temp_csv_path} has been deleted.")
    else:
        print(f"Temporary CSV file {temp_csv_path} does not exist.")

    # 删除另一个生成的CSV文件
    refinitiv_csv_path = f'./Output/{uuid}-refinitiv.csv'
    if os.path.exists(refinitiv_csv_path):
        os.remove(refinitiv_csv_path)
        print(f"Refinitiv CSV file {refinitiv_csv_path} has been deleted.")
    else:
        print(f"Refinitiv CSV file {refinitiv_csv_path} does not exist.")
