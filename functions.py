import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def calculate_estimated_change(row, coef_dict):
    return (row['avg_stableBorrowRate_eth_rates'] * coef_dict['avg_stableBorrowRate_eth_rates'] +
            row['avg_supplyRate_eth_rates'] * coef_dict['avg_supplyRate_eth_rates'] +
            row['weekly_change_usdc'] * coef_dict['weekly_change_usdc'] +
            row['deposits_volume_v3_eth_daily_deposits_borrows_ma_21'] * coef_dict['deposits_volume_v3_eth_daily_deposits_borrows_ma_21'] +
            row['price_eth'] * coef_dict['price_eth'] +
            row['moving_average_14_price_eth'] * coef_dict['moving_average_14_price_eth'] +
            row['deposits_volume_v3_eth_daily_deposits_borrows_ma_14'] * coef_dict['deposits_volume_v3_eth_daily_deposits_borrows_ma_14'] +
            row['moving_average_21_price_eth'] * coef_dict['moving_average_21_price_eth'] +
            row['avg_stableBorrowRate_eth_rates_ma_7'] * coef_dict['avg_stableBorrowRate_eth_rates_ma_7'] +
            row['avg_supplyRate_eth_rates_ma_7'] * coef_dict['avg_supplyRate_eth_rates_ma_7'])

def transpose_and_rename(csv_file_path, output_file_path):
    # load the CSV file
    df = pd.read_csv(csv_file_path)

    # Transpose the DataFrame
    transposed_df = df.transpose()

    # Reset the index to correctly handle columns after transposition
    transposed_df.reset_index(drop=True, inplace=True)

    # Generate new column names based on the 'looping_number' pattern
    new_column_names = [f'looping_{i+1}' for i in range(transposed_df.shape[1])]
    transposed_df.columns = new_column_names

    # Save the transposed and renamed DataFrame to a new CSV file
    transposed_df.to_csv(output_file_path, index=False)

    # Optionally print the final DataFrame to verify
    print(transposed_df.head())

def price_variation_graph(df):
    df['date_eth_volume'] = pd.to_datetime(df['date_eth_volume'])
    df.sort_values('date_eth_volume', inplace=True)

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(15, 7))  # Create the figure and axes for the graph
    sns.lineplot(ax=ax, x='date_eth_volume', y='price_eth', data=df)
    ax.set_title('ETH Price variation in the time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Locator automático
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Formato de fecha

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('./images/eth_price_variation_in_time.png')
    plt.show()