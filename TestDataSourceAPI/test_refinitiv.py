import json
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
def ref_market_signal(rics):
    output_dir = "./Output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize Refinitiv session
    os.environ["RD_LIB_CONFIG_PATH"] = "../Configuration"
    rd.open_session()

    signals = []  # 用于存储每个RIC信号的列表
    if isinstance(rics, str):
        rics = json.loads(rics)
    for item_id in rics.keys():
        # 假设rd.get_history能够返回与item_id相关的股票历史数据
        # 因为我们无法实际调用rd.get_history，所以这里用伪代码表示
        stock_data = rd.get_history(universe=item_id)

        # 将stock_data转换为DataFrame
        df = pd.DataFrame(stock_data)

        # 获取最后两个交易价格
        last_two_prices = df["TRDPRC_1"][-2:].values

        # 计算价格差异
        price_difference = last_two_prices[1] - last_two_prices[0]

        # 根据价格差异确定信号
        signal = price_difference/last_two_prices[1]
        signal = signal * 100
        signal = round(signal, 2)


        # 将信号添加到结果列表中
        signals.append(signal)

    return signals


