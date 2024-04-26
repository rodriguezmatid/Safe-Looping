import pandas as pd, numpy as np

start_date = "2023-01-26"
end_date = "2024-01-24"

# Loading the data
df_daily_deposits_borrows_v3 = pd.read_csv('datasets/aave_daily_deposits_borrows_v3.csv')
df_rates = pd.read_csv('datasets/aave_daily_rates.csv')
# df_liq_v3 = pd.read_csv('datasets/aave_liquidations_v3.csv')
df_volume = pd.read_csv('datasets/tokens_daily_volume.csv')
# df_ohcl = pd.read_csv('datasets/tokens_ohcl.csv')

# Filtering the data
df_daily_deposits_borrows_v3_eth = df_daily_deposits_borrows_v3.loc[df_daily_deposits_borrows_v3['symbol'] == 'WETH']
df_daily_deposits_borrows_v3_usdc = df_daily_deposits_borrows_v3.loc[df_daily_deposits_borrows_v3['symbol'] == 'USDC']

df_rates_eth = df_rates.loc[df_rates['symbol'] == 'WETH']
df_rates_usdc = df_rates.loc[df_rates['symbol'] == 'USDC']

df_volume_eth = df_volume.loc[df_volume['token'] == 'WETH']
df_volume_usdc = df_volume.loc[df_volume['token'] == 'USDC']

columns_rename_daily_deposits_borrows_v3_eth = {
    'day': 'date_eth_daily_deposits_borrows_v3',
    'symbol': 'symbol_v3_eth_daily_deposits_borrows',
    'contract_address': 'contract_address_v3_eth_daily_deposits_borrows',
    'deposits_volume': 'deposits_volume_v3_eth_daily_deposits_borrows',
    'borrows_volume': 'borrows_volume_v3_eth_daily_deposits_borrows'
}
columns_rename_daily_deposits_borrows_v3_usdc = {
    'day': 'date_usdc_daily_deposits_borrows_v3',
    'symbol': 'symbol_v3_usdc_daily_deposits_borrows',
    'contract_address': 'contract_address_v3_usdc_daily_deposits_borrows',
    'deposits_volume': 'deposits_volume_v3_usdc_daily_deposits_borrows',
    'borrows_volume': 'borrows_volume_v3_usdc_daily_deposits_borrows'
}
columns_rename_rates_eth = {
    'date': 'date_eth_rates',
    'symbol': 'symbol_eth_rates',
    'contract_address': 'contract_address_eth_rates',
    'avg_stableBorrowRate': 'avg_stableBorrowRate_eth_rates',
    'avg_variableBorrowRate': 'avg_variableBorrowRate_eth_rates',
    'avg_supplyRate': 'avg_supplyRate_eth_rates',
    'avg_liquidityIndex': 'avg_liquidityIndex_eth_rates',
    'avg_variableBorrowIndex': 'avg_variableBorrowIndex_eth_rates'
}
columns_rename_rates_usdc = {
    'date': 'date_usdc_rates',
    'symbol': 'symbol_usdc_rates',
    'contract_address': 'contract_address_usdc_rates',
    'avg_stableBorrowRate': 'avg_stableBorrowRate_usdc_rates',
    'avg_variableBorrowRate': 'avg_variableBorrowRate_usdc_rates',
    'avg_supplyRate': 'avg_supplyRate_usdc_rates',
    'avg_liquidityIndex': 'avg_liquidityIndex_usdc_rates',
    'avg_variableBorrowIndex': 'avg_variableBorrowIndex_usdc_rates'
}
columns_rename_volume_eth = {
    'date': 'date_eth_volume',
    'price': 'price_eth',
    'market_cap': 'market_cap_eth_volume',
    'volumes_last_24h': 'volumes_last_24h_eth_volume',
    'token': 'token_eth_volume'
}
columns_rename_volume_usdc = {
    'date': 'date_usdc_volume',
    'price': 'price_usdc',
    'market_cap': 'market_cap_usdc_volume',
    'volumes_last_24h': 'volumes_last_24h_usdc_volume',
    'token': 'token_usdc_volume'
}


# Columns replacement
df_daily_deposits_borrows_v3_eth = df_daily_deposits_borrows_v3_eth.rename(columns=columns_rename_daily_deposits_borrows_v3_eth)
df_daily_deposits_borrows_v3_usdc = df_daily_deposits_borrows_v3_usdc.rename(columns=columns_rename_daily_deposits_borrows_v3_usdc)
df_rates_eth = df_rates_eth.rename(columns=columns_rename_rates_eth)
df_rates_usdc = df_rates_usdc.rename(columns=columns_rename_rates_usdc)
df_volume_eth = df_volume_eth.rename(columns=columns_rename_volume_eth)
df_volume_usdc = df_volume_usdc.rename(columns=columns_rename_volume_usdc)

# Using df_volume_eth as base
base_df = df_volume_eth

# Combining the datasets with the base
dfs_to_merge = [
    (df_daily_deposits_borrows_v3_eth, 'date_eth_daily_deposits_borrows_v3'),
    (df_daily_deposits_borrows_v3_usdc, 'date_usdc_daily_deposits_borrows_v3'),
    (df_rates_eth, 'date_eth_rates'),
    (df_rates_usdc, 'date_usdc_rates'),
    (df_volume_usdc, 'date_usdc_volume')
]

for df, date_col in dfs_to_merge:
    base_df = pd.merge(base_df, df, left_on='date_eth_volume', right_on=date_col, how='left')

date_cols_to_drop = [date_col for _, date_col in dfs_to_merge if date_col != 'date_eth_volume'] # cleaning the other dates
base_df.drop(columns=date_cols_to_drop, inplace=True, errors='ignore')

columns_to_drop = ['token_eth_volume', 'symbol_v3_eth_daily_deposits_borrows', 'contract_address_v3_eth_daily_deposits_borrows', 'symbol_v3_usdc_daily_deposits_borrows', 'contract_address_v3_usdc_daily_deposits_borrows', 'symbol_eth_rates', 'contract_address_eth_rates', 'symbol_usdc_rates', 'contract_address_usdc_rates', 'token_usdc_volume', 'token_eth_ohcl', 'token_usdc_ohcl']

base_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

filtered_df = base_df[(base_df['date_eth_volume'] > start_date) & (base_df['date_eth_volume'] < end_date)].copy()

# Calculate the weekly price change
filtered_df['weekly_change_eth'] = np.log(filtered_df['price_eth'] / filtered_df['price_eth'].shift(7))
filtered_df['weekly_change_usdc'] = (filtered_df['price_usdc'] - filtered_df['price_usdc'].shift(7)) / filtered_df['price_usdc'].shift(7)

# Calculate the minimum price over the next 7 days
filtered_df['min_price_next_7_days_eth'] = filtered_df['price_eth'].rolling(window=7, min_periods=1).min()
filtered_df['min_price_next_7_days_usdc'] = filtered_df['price_usdc'].rolling(window=7, min_periods=1).min()

# Calculate the moving averages
filtered_df['moving_average_7_price_eth'] = filtered_df['price_eth'].rolling(window=7, min_periods=1).mean()
filtered_df['moving_average_14_price_eth'] = filtered_df['price_eth'].rolling(window=14, min_periods=1).mean()
filtered_df['moving_average_21_price_eth'] = filtered_df['price_eth'].rolling(window=21, min_periods=1).mean()
filtered_df['moving_average_30_price_eth'] = filtered_df['price_eth'].rolling(window=30, min_periods=1).mean()

filtered_df['moving_average_7_volume_eth'] = filtered_df['volumes_last_24h_eth_volume'].rolling(window=7, min_periods=1).mean()
filtered_df['moving_average_14_volume_eth'] = filtered_df['volumes_last_24h_eth_volume'].rolling(window=14, min_periods=1).mean()
filtered_df['moving_average_21_volume_eth'] = filtered_df['volumes_last_24h_eth_volume'].rolling(window=21, min_periods=1).mean()
filtered_df['moving_average_30_volume_eth'] = filtered_df['volumes_last_24h_eth_volume'].rolling(window=30, min_periods=1).mean()

filtered_df['moving_average_7_mc_eth'] = filtered_df['market_cap_eth_volume'].rolling(window=7, min_periods=1).mean()
filtered_df['moving_average_14_mc_eth'] = filtered_df['market_cap_eth_volume'].rolling(window=14, min_periods=1).mean()
filtered_df['moving_average_21_mc_eth'] = filtered_df['market_cap_eth_volume'].rolling(window=21, min_periods=1).mean()
filtered_df['moving_average_30_mc_eth'] = filtered_df['market_cap_eth_volume'].rolling(window=30, min_periods=1).mean()

filtered_df['deposits_volume_v3_eth_daily_deposits_borrows_ma_7'] = filtered_df['deposits_volume_v3_eth_daily_deposits_borrows'].rolling(window=7, min_periods=1).mean()
filtered_df['deposits_volume_v3_eth_daily_deposits_borrows_ma_14'] = filtered_df['deposits_volume_v3_eth_daily_deposits_borrows'].rolling(window=14, min_periods=1).mean()
filtered_df['deposits_volume_v3_eth_daily_deposits_borrows_ma_21'] = filtered_df['deposits_volume_v3_eth_daily_deposits_borrows'].rolling(window=21, min_periods=1).mean()
filtered_df['deposits_volume_v3_eth_daily_deposits_borrows_ma_30'] = filtered_df['deposits_volume_v3_eth_daily_deposits_borrows'].rolling(window=30, min_periods=1).mean()

filtered_df['borrows_volume_v3_eth_daily_deposits_borrows_ma_7'] = filtered_df['borrows_volume_v3_eth_daily_deposits_borrows'].rolling(window=7, min_periods=1).mean()
filtered_df['borrows_volume_v3_eth_daily_deposits_borrows_ma_14'] = filtered_df['borrows_volume_v3_eth_daily_deposits_borrows'].rolling(window=14, min_periods=1).mean()
filtered_df['borrows_volume_v3_eth_daily_deposits_borrows_ma_21'] = filtered_df['borrows_volume_v3_eth_daily_deposits_borrows'].rolling(window=21, min_periods=1).mean()
filtered_df['borrows_volume_v3_eth_daily_deposits_borrows_ma_30'] = filtered_df['borrows_volume_v3_eth_daily_deposits_borrows'].rolling(window=30, min_periods=1).mean()

filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows_ma_7'] = filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows'].rolling(window=7, min_periods=1).mean()
filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows_ma_14'] = filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows'].rolling(window=14, min_periods=1).mean()
filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows_ma_21'] = filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows'].rolling(window=21, min_periods=1).mean()
filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows_ma_30'] = filtered_df['deposits_volume_v3_usdc_daily_deposits_borrows'].rolling(window=30, min_periods=1).mean()

filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows_ma_7'] = filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows'].rolling(window=7, min_periods=1).mean()
filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows_ma_14'] = filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows'].rolling(window=14, min_periods=1).mean()
filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows_ma_21'] = filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows'].rolling(window=21, min_periods=1).mean()
filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows_ma_30'] = filtered_df['borrows_volume_v3_usdc_daily_deposits_borrows'].rolling(window=30, min_periods=1).mean()

filtered_df['avg_stableBorrowRate_eth_rates_ma_7'] = filtered_df['avg_stableBorrowRate_eth_rates'].rolling(window=7, min_periods=1).mean()
filtered_df['avg_stableBorrowRate_eth_rates_ma_14'] = filtered_df['avg_stableBorrowRate_eth_rates'].rolling(window=14, min_periods=1).mean()
filtered_df['avg_stableBorrowRate_eth_rates_ma_21'] = filtered_df['avg_stableBorrowRate_eth_rates'].rolling(window=21, min_periods=1).mean()
filtered_df['avg_stableBorrowRate_eth_rates_ma_30'] = filtered_df['avg_stableBorrowRate_eth_rates'].rolling(window=30, min_periods=1).mean()

filtered_df['avg_variableBorrowRate_eth_rates_ma_7'] = filtered_df['avg_variableBorrowRate_eth_rates'].rolling(window=7, min_periods=1).mean()
filtered_df['avg_variableBorrowRate_eth_rates_ma_14'] = filtered_df['avg_variableBorrowRate_eth_rates'].rolling(window=14, min_periods=1).mean()
filtered_df['avg_variableBorrowRate_eth_rates_ma_21'] = filtered_df['avg_variableBorrowRate_eth_rates'].rolling(window=21, min_periods=1).mean()
filtered_df['avg_variableBorrowRate_eth_rates_ma_30'] = filtered_df['avg_variableBorrowRate_eth_rates'].rolling(window=30, min_periods=1).mean()

filtered_df['avg_supplyRate_eth_rates_ma_7'] = filtered_df['avg_supplyRate_eth_rates'].rolling(window=7, min_periods=1).mean()
filtered_df['avg_supplyRate_eth_rates_ma_14'] = filtered_df['avg_supplyRate_eth_rates'].rolling(window=14, min_periods=1).mean()
filtered_df['avg_supplyRate_eth_rates_ma_21'] = filtered_df['avg_supplyRate_eth_rates'].rolling(window=21, min_periods=1).mean()
filtered_df['avg_supplyRate_eth_rates_ma_30'] = filtered_df['avg_supplyRate_eth_rates'].rolling(window=30, min_periods=1).mean()

filtered_df['avg_liquidityIndex_eth_rates_ma_7'] = filtered_df['avg_liquidityIndex_eth_rates'].rolling(window=7, min_periods=1).mean()
filtered_df['avg_liquidityIndex_eth_rates_ma_14'] = filtered_df['avg_liquidityIndex_eth_rates'].rolling(window=14, min_periods=1).mean()
filtered_df['avg_liquidityIndex_eth_rates_ma_21'] = filtered_df['avg_liquidityIndex_eth_rates'].rolling(window=21, min_periods=1).mean()
filtered_df['avg_liquidityIndex_eth_rates_ma_30'] = filtered_df['avg_liquidityIndex_eth_rates'].rolling(window=30, min_periods=1).mean()

filtered_df['avg_variableBorrowIndex_eth_rates_ma_7'] = filtered_df['avg_variableBorrowIndex_eth_rates'].rolling(window=7, min_periods=1).mean()
filtered_df['avg_variableBorrowIndex_eth_rates_ma_14'] = filtered_df['avg_variableBorrowIndex_eth_rates'].rolling(window=14, min_periods=1).mean()
filtered_df['avg_variableBorrowIndex_eth_rates_ma_21'] = filtered_df['avg_variableBorrowIndex_eth_rates'].rolling(window=21, min_periods=1).mean()
filtered_df['avg_variableBorrowIndex_eth_rates_ma_30'] = filtered_df['avg_variableBorrowIndex_eth_rates'].rolling(window=30, min_periods=1).mean()

filtered_df['moving_average_7_price_usdc'] = filtered_df['price_usdc'].rolling(window=7, min_periods=1).mean()
filtered_df['moving_average_14_price_usdc'] = filtered_df['price_usdc'].rolling(window=14, min_periods=1).mean()
filtered_df['moving_average_21_price_usdc'] = filtered_df['price_usdc'].rolling(window=21, min_periods=1).mean()
filtered_df['moving_average_30_price_usdc'] = filtered_df['price_usdc'].rolling(window=30, min_periods=1).mean()

# Saving filtered_df to a CSV
filtered_df.to_csv('./results/final_combined_dataset.csv', index=False)