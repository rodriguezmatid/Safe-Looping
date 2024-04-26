import pandas as pd

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