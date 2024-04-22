import pandas as pd
import os

# Cargar todos los dataframes
df_daily_deposits_borrows_v2 = pd.read_csv('datasets/aave_daily_deposits_borrows_v2.csv')
df_daily_deposits_borrows_v3 = pd.read_csv('datasets/aave_daily_deposits_borrows_v3.csv')
df_rates = pd.read_csv('datasets/aave_daily_rates.csv')
# df_liq_v2 = pd.read_csv('datasets/aave_liquidations_v2.csv')
# df_liq_v3 = pd.read_csv('datasets/aave_liquidations_v3.csv')
df_volume = pd.read_csv('datasets/tokens_daily_volume.csv')
df_ohcl = pd.read_csv('datasets/tokens_ohcl.csv')

df_daily_deposits_borrows_v2_eth = df_daily_deposits_borrows_v2.loc[df_daily_deposits_borrows_v2['symbol'] == 'WETH']
df_daily_deposits_borrows_v2_usdc = df_daily_deposits_borrows_v2.loc[df_daily_deposits_borrows_v2['symbol'] == 'USDC']

df_daily_deposits_borrows_v3_eth = df_daily_deposits_borrows_v3.loc[df_daily_deposits_borrows_v3['symbol'] == 'WETH']
df_daily_deposits_borrows_v3_usdc = df_daily_deposits_borrows_v3.loc[df_daily_deposits_borrows_v3['symbol'] == 'USDC']

df_rates_eth = df_rates.loc[df_rates['symbol'] == 'WETH']
df_rates_usdc = df_rates.loc[df_rates['symbol'] == 'USDC']

df_volume_eth = df_volume.loc[df_volume['token'] == 'WETH']
df_volume_usdc = df_volume.loc[df_volume['token'] == 'USDC']

df_ohcl_eth = df_ohcl.loc[df_ohcl['token'] == 'WETH']
df_ohcl_usdc = df_ohcl.loc[df_ohcl['token'] == 'USDC']

# Columns rename
columns_rename_daily_deposits_borrows_v2_eth = {
    'day': 'date_eth_daily_deposits_borrows_v2',
    'symbol': 'symbol_v2_eth_daily_deposits_borrows',
    'contract_address': 'contract_address_v2_eth_daily_deposits_borrows',
    'deposits_volume': 'deposits_volume_v2_eth_daily_deposits_borrows',
    'borrows_volume': 'borrows_volume_v2_eth_daily_deposits_borrows'
}

columns_rename_daily_deposits_borrows_v2_usdc = {
    'day': 'date_usdc_daily_deposits_borrows_v2',
    'symbol': 'symbol_v2_usdc_daily_deposits_borrows',
    'contract_address': 'contract_address_v2_usdc_daily_deposits_borrows',
    'deposits_volume': 'deposits_volume_v2_usdc_daily_deposits_borrows',
    'borrows_volume': 'borrows_volume_v2_usdc_daily_deposits_borrows'
}

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
    'price': 'price_eth_volume',
    'market_cap': 'market_cap_eth_volume',
    'volumes_last_24h': 'volumes_last_24h_eth_volume',
    'token': 'token_eth_volume'
}

columns_rename_volume_usdc = {
    'date': 'date_usdc_volume',
    'price': 'price_usdc_volume',
    'market_cap': 'market_cap_usdc_volume',
    'volumes_last_24h': 'volumes_last_24h_usdc_volume',
    'token': 'token_usdc_volume'
}

columns_rename_ohcl_eth = {
    'date': 'date_eth_ohcl',
    'open': 'open_eth_ohcl',
    'high': 'high_eth_ohcl',
    'low': 'low_eth_ohcl',
    'close': 'close_eth_ohcl',
    'token': 'token_eth_ohcl'
}

columns_rename_ohcl_usdc = {
    'date': 'date_usdc_ohcl',
    'open': 'open_usdc_ohcl',
    'high': 'high_usdc_ohcl',
    'low': 'low_usdc_ohcl',
    'close': 'close_usdc_ohcl',
    'token': 'token_usdc_ohcl'
}

# Columns replacement
df_daily_deposits_borrows_v2_eth = df_daily_deposits_borrows_v2_eth.rename(columns=columns_rename_daily_deposits_borrows_v2_eth)
df_daily_deposits_borrows_v2_usdc = df_daily_deposits_borrows_v2_usdc.rename(columns=columns_rename_daily_deposits_borrows_v2_usdc)
df_daily_deposits_borrows_v3_eth = df_daily_deposits_borrows_v3_eth.rename(columns=columns_rename_daily_deposits_borrows_v3_eth)
df_daily_deposits_borrows_v3_usdc = df_daily_deposits_borrows_v3_usdc.rename(columns=columns_rename_daily_deposits_borrows_v3_usdc)
df_rates_eth = df_rates_eth.rename(columns=columns_rename_rates_eth)
df_rates_usdc = df_rates_usdc.rename(columns=columns_rename_rates_usdc)
df_volume_eth = df_volume_eth.rename(columns=columns_rename_volume_eth)
df_volume_usdc = df_volume_usdc.rename(columns=columns_rename_volume_usdc)
df_ohcl_eth = df_ohcl_eth.rename(columns=columns_rename_ohcl_eth)
df_ohcl_usdc = df_ohcl_usdc.rename(columns=columns_rename_ohcl_usdc)

# Usar df_volume_eth como base
base_df = df_volume_eth

# Lista de dataframes para combinar con la base, junto con sus columnas de fecha renombradas
dfs_to_merge = [
    (df_daily_deposits_borrows_v2_eth, 'date_eth_daily_deposits_borrows_v2'),
    (df_daily_deposits_borrows_v2_usdc, 'date_usdc_daily_deposits_borrows_v2'),
    (df_daily_deposits_borrows_v3_eth, 'date_eth_daily_deposits_borrows_v3'),
    (df_daily_deposits_borrows_v3_usdc, 'date_usdc_daily_deposits_borrows_v3'),
    (df_rates_eth, 'date_eth_rates'),
    (df_rates_usdc, 'date_usdc_rates'),
    (df_volume_usdc, 'date_usdc_volume'),
    (df_ohcl_eth, 'date_eth_ohcl'),
    (df_ohcl_usdc, 'date_usdc_ohcl')
]

# Realizar los joins sucesivos
for df, date_col in dfs_to_merge:
    base_df = pd.merge(base_df, df, left_on='date_eth_volume', right_on=date_col, how='left')

# Opcional: limpiar columnas de fecha adicionales que ya no se necesitan
date_cols_to_drop = [date_col for _, date_col in dfs_to_merge if date_col != 'date_eth_volume']
base_df.drop(columns=date_cols_to_drop, inplace=True, errors='ignore')

# Guardar el DataFrame final combinado
base_df.to_csv('datasets/final_combined_dataset.csv', index=False)