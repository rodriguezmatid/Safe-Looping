import pandas as pd

# Configuration to display only two decimals in floats
pd.set_option('display.float_format', '{:.2f}'.format)

# Parameters
initial_eth_amount = 1
max_ltv = 1.20
supply_apy_eth = 0.03
borrow_apy_usdc = 0.13
usdc_price = 1
liquidation_threshold = 0.8
times_liquidated = 0

# Dataframes
columns = ['Start Day', 'Loop', 'Day', 'eth_price', 'Total_token_supply', 'Total_token_supply_mktv', 'Total_token_borrow', 'LTV', 'Liquidated']
results_df = pd.DataFrame(columns=columns)

# Rates data
data_rates = pd.read_csv('./datasets/aave_daily_rates.csv')
filtered_data_rates = data_rates.loc[(data_rates['symbol'] == 'WETH') | (data_rates['symbol'] == 'USDC'), ['date', 'symbol', 'avg_stableBorrowRate', 'avg_variableBorrowRate', 'avg_supplyRate']]
filtered_data_rates['date'] = pd.to_datetime(filtered_data_rates['date'])
sorted_data_rates = filtered_data_rates.sort_values(by='date', ascending=False)

# Borrow rates
filtered_borrow_rates = sorted_data_rates.loc[(sorted_data_rates['symbol'] == 'USDC'), ['date', 'symbol', 'avg_stableBorrowRate']]
last_365_days_sorted_data_rates_borrow = filtered_borrow_rates.head(7)
sorted_last_365_days_data_rates_borrow = last_365_days_sorted_data_rates_borrow.sort_values(by='date', ascending=True)
borrow_rate_list = sorted_last_365_days_data_rates_borrow['avg_stableBorrowRate'].tolist()
print(borrow_rate_list)

# Supply rates
filtered_supply_rates = sorted_data_rates.loc[(sorted_data_rates['symbol'] == 'WETH'), ['date', 'symbol', 'avg_supplyRate']]
last_365_days_sorted_data_rates_supply = filtered_supply_rates.head(7)
sorted_last_365_days_data_rates_supply = last_365_days_sorted_data_rates_supply.sort_values(by='date', ascending=True)
supply_rate_list = sorted_last_365_days_data_rates_supply['avg_supplyRate'].tolist()
print(supply_rate_list)

# Prices Data
data_prices = pd.read_csv('./datasets/tokens_ohcl.csv')
filtered_data_prices = data_prices.loc[data_prices['token'] == 'WETH', ['date', 'low', 'token']]
filtered_data_prices['date'] = pd.to_datetime(filtered_data_prices['date'])
sorted_data_prices = filtered_data_prices.sort_values(by='date', ascending=False)
last_365_days_sorted_data_prices = sorted_data_prices.head(len(supply_rate_list))
sorted_last_365_days_data_prices = last_365_days_sorted_data_prices.sort_values(by='date', ascending=True)

eth_price_changes = sorted_last_365_days_data_prices['low'].tolist()
eth_price_changes = [1598.16, 1350, 2000, 1700, 1630, 1200, 1400]
print(eth_price_changes)

num_days = len(eth_price_changes)

# Proceso de cada día tomando una nueva posición
for start_day in range(num_days):
    liquidated_in_previous_loop = False
    for loop in range(1, 6):

        # Reiniciar valores al inicio de cada nuevo día de posición
        total_eth_supplied = initial_eth_amount
        total_usdc_borrowed = 0
        eth_price = eth_price_changes[start_day]

        # Bucle de préstamos solo el primer día de cada nueva posición
        for _ in range(loop):
            total_token_borrow_previous_loop = total_usdc_borrowed
            total_token_supply_previous_loop = total_eth_supplied

            usdc_borrowed = total_token_supply_previous_loop * eth_price * (1/max_ltv) - total_token_borrow_previous_loop
            total_usdc_borrowed = total_token_borrow_previous_loop + usdc_borrowed

            extra_eth_supplied = usdc_borrowed / eth_price
            total_eth_supplied = total_token_supply_previous_loop + extra_eth_supplied

            # Calcular LTV inicial
            total_supply_mkt_value = total_eth_supplied * eth_price
            ltv = total_usdc_borrowed / total_supply_mkt_value

            # Almacenar los resultados del primer día de préstamos
            new_row = pd.DataFrame({
                'Start Day': [start_day],
                'Loop': [loop],
                'Day': [0],  # El primer día siempre es 0
                'eth_price': [eth_price],
                'Total_token_supply': [total_eth_supplied],
                'Total_token_supply_mktv': [total_supply_mkt_value],
                'Total_token_borrow': [total_usdc_borrowed],
                'LTV': [ltv],
                'Liquidated': [False]
            })
            results_df = pd.concat([results_df, new_row], ignore_index=True)

        total_token_borrow = total_usdc_borrowed
        total_token_supply = total_eth_supplied

        # Simulación para los próximos 7 días
        for day in range(1, min(7, num_days - start_day)):
            day_index = start_day + day
            eth_price = eth_price_changes[day_index]
            total_token_borrow = total_token_borrow * (1 + borrow_apy_usdc/365)
            total_token_supply = total_token_supply * (1 + supply_apy_eth/365)

            total_market_value_borrow = total_token_borrow
            total_market_value_supply = total_token_supply * eth_price

            ltv = total_market_value_borrow/total_market_value_supply

            if ltv > liquidation_threshold:
                liquidated = True
                times_liquidated += 1
                liquidated_in_previous_loop = True
                print(f"Liquidated position started on day {start_day}, on loop {loop}, on day {day}")
            else:
                liquidated = False

            # Almacenar los resultados diarios
            new_row = pd.DataFrame({
                'Start Day': [start_day],
                'Loop': [loop],
                'Day': [day],  # Días subsecuentes
                'eth_price': [eth_price],
                'Total_token_supply': [total_token_supply],
                'Total_token_supply_mktv': [total_market_value_supply],
                'Total_token_borrow': [total_market_value_borrow],
                'LTV': [ltv],
                'Liquidated': [liquidated]
            })
            results_df = pd.concat([results_df, new_row], ignore_index=True)

            if liquidated:
                break

# Configuración para mostrar más filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)  # Ajustar el ancho de la pantalla

# Imprimir DataFrame completo y veces liquidadas
print(results_df)
print("Times liquidated:", times_liquidated)
# Guardar el DataFrame en un archivo CSV
results_df.to_csv('results.csv', index=False)


# Crear DataFrame resumen para las liquidaciones
summary_df = pd.DataFrame(0, index=[f'Loop {i}' for i in range(1, 6)], columns=[f'Start Day {i}' for i in range(num_days)])

# Rellenar el DataFrame resumen con los datos de liquidación
for loop in range(1, 6):
    for start_day in range(num_days):
        # Comprobar si hubo alguna liquidación en la serie de 7 días siguientes a start_day
        liquidated = results_df[(results_df['Start Day'] == start_day) & (results_df['Loop'] == loop) & (results_df['Liquidated'])]['Liquidated'].any()
        summary_df.at[f'Loop {loop}', f'Start Day {start_day}'] = 1 if liquidated else 0

# Imprimir el DataFrame resumen
print(summary_df)
summary_df.to_csv('dummy_matrix.csv', index=False)