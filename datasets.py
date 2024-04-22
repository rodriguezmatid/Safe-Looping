from giza_datasets import DatasetsHub, DatasetsLoader
import pandas as pd, os, certifi, polars as pl
loader = DatasetsLoader()

os.environ['SSL_CERT_FILE'] = certifi.where()

hub = DatasetsHub()
hub.show()

# datasets = hub.list()
# print(datasets)

# ###################################
# # Daily Exchange Rates & Indexes v3

# # This dataset provides the average borrowing rates (variable & stable), supply rate, and liquidity indexes of Aave v2 Lending Pools. Only the pools in Ethereum L1 are considered, and the contract_address feature can be used as a unique identifier for the individual pools. The dataset contains all the pool data from 25.01.2023 to 25.01.2024, and individual rows are omitted if there were borrows executed on the pool.

df_aave_daily_rates = loader.load('aave-daily-rates-indexes')
# print(df_aave_daily_rates)

data_aave_daily_rates = pd.DataFrame(df_aave_daily_rates, columns=['date', 'symbol', 'contract_address', 'avg_stableBorrowRate', 'avg_variableBorrowRate', 'avg_supplyRate', 'avg_liquidityIndex', 'avg_variableBorrowIndex'])

data_aave_daily_rates.to_csv('datasets/aave_daily_rates.csv', index=False)

# ###################################
# # Tokens OHLC price

# # This dataset contains each 4 days historical price data for various cryptocurrencies, sourced from the CoinGecko API. It includes data fields such as Open, High, Low, Close, and token

df_tokens_ohcl = loader.load('tokens-ohcl')
# print(df_tokens_ohcl)

# Convierte la columna de fecha a string en Polars
df_tokens_ohcl = df_tokens_ohcl.with_columns(
    df_tokens_ohcl['date'].cast(pl.datatypes.Utf8)
)

data_tokens_ohcl = df_tokens_ohcl.to_pandas()

data_tokens_ohcl = pd.DataFrame(df_tokens_ohcl, columns=['date', 'open', 'high', 'low', 'close', 'token'])
data_tokens_ohcl.to_csv('datasets/tokens_ohcl.csv', index=False)

# ###################################
# # Daily Deposits & Borrows
# This dataset provides the aggregated daily borrows and deposits made to the Aave Lending Pools. Only the pools in Ethereum L1 are taken into account and the contract_address feature can be used as an unique identifier for the individual pools. The dataset contains all the pool data from 25.01.2023 to 25.01.2024, and individual rows are omitted if there were no borrows or deposits made in a given day. 

# Daily Deposits & Borrows v2

df_aave_daily_deposits_borrows_v2 = loader.load('aave-daily-deposits-borrowsv2')
# print(df_aave_daily_deposits_borrows_v2)

data_aave_daily_deposits_borrows_v2 = pd.DataFrame(df_aave_daily_deposits_borrows_v2, columns=['day', 'symbol', 'contract_address', 'deposits_volume', 'borrows_volume'])

data_aave_daily_deposits_borrows_v2.to_csv('datasets/aave_daily_deposits_borrows_v2.csv', index=False)

# # Daily Deposits & Borrows v3

df_aave_daily_deposits_borrows_v3 = loader.load('aave-daily-deposits-borrowsv3')
# print(df_aave_daily_deposits_borrows_v3)

data_aave_daily_deposits_borrows_v3 = pd.DataFrame(df_aave_daily_deposits_borrows_v3, columns=['day', 'symbol', 'contract_address', 'deposits_volume', 'borrows_volume'])

data_aave_daily_deposits_borrows_v3.to_csv('datasets/aave_daily_deposits_borrows_v3.csv', index=False)

# ###################################
# Aave liquidations

# This dataset contains all the individual liquidations of borrow positions in the Aave Protocol. Only the liquidations in Ethereum L1 are shown and the dataset contains all the liquidation data from inception to 05.02.2024.

# Aave Liquidations v2

df_aave_liquidations_v2 = loader.load('aave-liquidationsV2')
# print(df_aave_liquidations_v2)

data_aave_liquidations_v2 = pd.DataFrame(df_aave_liquidations_v2, columns=['day', 'liquidator', 'user', 'token_col', 'token_debt', 'col_contract_address', 'collateral_amount', 'col_value_USD', 'col_current_value_USD','debt_contract_address', 'debt_amount', 'debt_value_USD', 'debt_current_value_USD'])

data_aave_liquidations_v2.to_csv('datasets/aave_liquidations_v2.csv', index=False)

# Aave Liquidations v3

df_aave_liquidations_v3 = loader.load('aave-liquidationsV3')
# print(df_aave_liquidations_v3)

data_aave_liquidations_v3 = pd.DataFrame(df_aave_liquidations_v3, columns=['day', 'liquidator', 'user', 'token_col', 'token_debt', 'col_contract_address', 'collateral_amount', 'col_value_USD', 'col_current_value_USD','debt_contract_address', 'debt_amount', 'debt_value_USD', 'debt_current_value_USD'])

data_aave_liquidations_v3.to_csv('datasets/aave_liquidations_v3.csv', index=False)

# ###################################
# Tokens daily prices volume

# This dataset contains daily historical price, mcap and 24h volumes data for various cryptocurrencies, sourced from the CoinGecko API. It includes data fields such as price, market_cap, volumes_last_24h  and token for each day.

df_tokens_daily_prices_volume = loader.load('tokens-daily-prices-mcap-volume')
# print(df_tokens_daily_prices_volume)
df_pandas = df_tokens_daily_prices_volume.to_pandas()

data_tokens_daily_prices_volume = pd.DataFrame(df_pandas, columns=['date', 'price', 'market_cap', 'volumes_last_24h', 'token'])
data_tokens_daily_prices_volume.to_csv('datasets/tokens_daily_volume.csv', index=False)