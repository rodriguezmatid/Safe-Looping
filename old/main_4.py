import pandas as pd

# Configuración para mostrar sólo dos decimales en los floats
pd.set_option('display.float_format', '{:.2f}'.format)

# Inicialización de parámetros
initial_eth_amount = 1
max_ltv = 1.20
supply_apy_eth = 0.03
borrow_apy_usdc = 0.13
usdc_price = 1
eth_price = 1598.16
liquidation_threshold = 0.8

eth_price_changes = [1598.16, 1805, 2000, 1700, 1630, 1200, 1400]  # Precios diarios

times_liquidated = 0

# DataFrame para guardar los resultados
columns = ['Start Day', 'Day', 'eth_price', 'Total_token_supply', 'Total_token_supply_mktv', 'Total_token_borrow', 'LTV']
results_df = pd.DataFrame(columns=columns)

num_days = len(eth_price_changes)  # Días disponibles para el análisis

# Proceso de cada día tomando una nueva posición y evaluando los próximos 7 días
for start_day in range(num_days):
    # Reiniciar valores al inicio de cada nuevo día de posición
    total_eth_supplied = initial_eth_amount
    usdc_borrowed = 0
    eth_price = eth_price_changes[start_day]

    # Bucle de préstamos solo el primer día de cada nueva posición
    for loop in range(4):
        if loop == 0:
            extra_eth_supplied = 0
            ltv = 0
        else:
            total_token_borrow_previous_loop = usdc_borrowed
            total_token_supply_previous_loop = total_eth_supplied
            
            usdc_borrowed = total_token_supply_previous_loop * eth_price * (1/max_ltv) - total_token_borrow_previous_loop
            total_usdc_borrowed = total_token_borrow_previous_loop + usdc_borrowed

            extra_eth_supplied = usdc_borrowed / eth_price
            total_eth_supplied = total_token_supply_previous_loop + extra_eth_supplied

        # Calcular LTV inicial
        total_supply_mkt_value = total_eth_supplied * eth_price
        ltv = usdc_borrowed / total_supply_mkt_value

        # Almacenar los resultados del primer día de préstamos
        new_row = pd.DataFrame({
            'Start Day': [start_day],
            'Day': [0],  # El primer día siempre es 0
            'eth_price': [eth_price],
            'Total_token_supply': [total_eth_supplied],
            'Total_token_supply_mktv': [total_supply_mkt_value],
            'Total_token_borrow': [usdc_borrowed],
            'LTV': [ltv]
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
            print(f"Liquidated position started on day {start_day}, on day {day}")
            times_liquidated += 1
            liquidated = True
        else:
            liquidated = False

        # Almacenar los resultados diarios
        new_row = pd.DataFrame({
            'Start Day': [start_day],
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

# Imprimir DataFrame completo y veces liquidadas
print(results_df)
print("Times liquidated:", times_liquidated)

# Crear DataFrame resumen para las liquidaciones
summary_df = pd.DataFrame(0, index=[0], columns=[f'Start Day {i}' for i in range(num_days)])

# Rellenar el DataFrame resumen con los datos de liquidación
for start_day in range(num_days):
    # Comprobar si hubo alguna liquidación en la serie de 7 días siguientes a start_day
    liquidated = results_df[(results_df['Start Day'] == start_day) & (results_df['Liquidated'])]['Liquidated'].any()
    summary_df[f'Start Day {start_day}'] = 1 if liquidated else 0

# Imprimir el DataFrame resumen
print(summary_df)