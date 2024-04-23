import pandas as pd

# Configuración para mostrar sólo dos decimales en los floats
pd.set_option('display.float_format', '{:.2f}'.format)

initial_eth_amount = 1
max_ltv = 1.20
supply_apy_eth = 0.03
borrow_apy_usdc = 0.13
usdc_price = 1
eth_price = 1598.16
liquidation_threshold = 0.8

eth_price_changes = [1598.16, 1805, 2000, 1700, 1630, 1200, 1400]  # Ajustado el precio del día 4

total_eth_supplied = initial_eth_amount
total_supply_mkt_value = eth_price * total_eth_supplied
usdc_borrowed = 0
total_usdc_borrowed = 0

times_liquidated = 0

columns = ['Day', 'eth_price', 'Total_token_supply', 'Total_token_supply_mktv', 'Total_token_borrow', 'LTV']
results_df = pd.DataFrame(columns=columns)

num_days = 6
loops_per_day = 4
liquidated = False

# Solo bucle de préstamos el primer día
for loop in range(loops_per_day):
    if loop == 0:
        extra_eth_supplied = 0
        ratio_colat = 0
        ltv = 0
    else:
        total_token_supply_previous_loop = total_eth_supplied
        total_token_borrow_previous_loop = total_usdc_borrowed
        usdc_borrowed = total_token_supply_previous_loop * eth_price * (1/max_ltv) - total_token_borrow_previous_loop
        extra_eth_supplied = usdc_borrowed / eth_price
        total_eth_supplied = total_token_supply_previous_loop + extra_eth_supplied
        total_supply_mkt_value = total_eth_supplied * eth_price
        total_usdc_borrowed = total_token_borrow_previous_loop + usdc_borrowed
        ratio_colat = total_supply_mkt_value / total_usdc_borrowed
        ltv = 1 / ratio_colat

    # Guardar resultados del primer día
    new_row = {
        'Day': 0,
        'eth_price': eth_price,
        'Total_token_supply': total_eth_supplied,
        'Total_token_supply_mktv': total_supply_mkt_value,
        'Total_token_borrow': total_usdc_borrowed,
        'LTV': ltv
    }
    results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)


total_token_borrow = total_usdc_borrowed
total_token_supply = total_eth_supplied

for day in range(1, num_days):
    eth_price = eth_price_changes[day]

    total_token_borrow = total_token_borrow * (1 + borrow_apy_usdc/365)
    total_token_supply = total_token_supply * (1 + supply_apy_eth/365)
    
    total_market_value_borrow = total_token_borrow
    total_market_value_supply = total_token_supply * eth_price
    
    ltv = total_market_value_borrow/total_market_value_supply
    
    if ltv > liquidation_threshold:
        print(f"Liquidated position on day {day}")
        print("ETH_price", eth_price)
        print("Total Supply", total_market_value_supply)
        print("Total Supply MKT v", total_market_value_supply)
        print("Total Borrowed", total_market_value_borrow)
        print("LTV", ltv)
        print("-------")
        liquidated = True
        times_liquidated += 1
        break

    # Guardar resultados de los días siguientes
    new_row = {
        'Day': day,
        'eth_price': eth_price,
        'Total_token_supply': total_token_supply,
        'Total_token_supply_mktv': total_market_value_supply,
        'Total_token_borrow': total_token_borrow,
        'LTV': ltv
    }

    results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

# Imprimir DataFrame completo
print(results_df)
print("Times liquidated: ", times_liquidated)
