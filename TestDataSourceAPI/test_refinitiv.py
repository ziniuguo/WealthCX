import os
import refinitiv.data as rd
import pandas as pd
import matplotlib.pyplot as plt

def generate_and_save_chart(uuid, item_id):
    # Ensure the output directory exists
    output_dir = "./Output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize Refinitiv session
    os.environ["RD_LIB_CONFIG_PATH"] = "../Configuration"
    rd.open_session()

    # Fetch stock price history
    stock_data = rd.get_history(universe=item_id)
    df = pd.DataFrame(stock_data)

    # Close Refinitiv session
    rd.close_session()

    # Generate the chart
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['TRDPRC_1'], marker='o', linestyle='-', color='blue')
    for x, y in zip(df.index, df['TRDPRC_1']):
        plt.text(x, y, f'{y:.2f}', color='black', ha='center', va='bottom')
    plt.title(f'{item_id} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('TRDPRC_1 Price')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the chart
    chart_path = os.path.join(output_dir, f"{uuid}.png")
    plt.savefig(chart_path)
    plt.close()  # Close the plot to free memory
    return chart_path

# x = generate_and_save_chart(1,"JPM")
