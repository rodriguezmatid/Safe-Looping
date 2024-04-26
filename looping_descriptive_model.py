import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
max_loop = 5

# Dataframes
columns = ['Start Day', 'Loop', 'Day', 'eth_price', 'Total_token_supply', 'Total_token_supply_mktv', 'Total_token_borrow', 'LTV', 'Liquidated']
results_df = pd.DataFrame(columns=columns)

# Rates data
data_rates = pd.read_csv('./results/final_combined_dataset.csv')
filtered_data_rates = data_rates[['date_eth_volume', 'avg_supplyRate_eth_rates', 'avg_stableBorrowRate_usdc_rates', 'price_eth']]
filtered_data_rates['date_eth_volume'] = pd.to_datetime(filtered_data_rates['date_eth_volume'])
sorted_data_rates = filtered_data_rates.sort_values(by='date_eth_volume', ascending=True)
print(sorted_data_rates.head())

# Borrow rates
filtered_borrow_rates = sorted_data_rates[['date_eth_volume', 'avg_stableBorrowRate_usdc_rates']]
# filtered_borrow_rates = filtered_borrow_rates.head(7)
borrow_rate_list = filtered_borrow_rates['avg_stableBorrowRate_usdc_rates'].tolist()
# print(borrow_rate_list)

# Supply rates
filtered_supply_rates = sorted_data_rates[['date_eth_volume', 'avg_supplyRate_eth_rates']]
# filtered_supply_rates = filtered_supply_rates.head(7)
supply_rate_list = filtered_supply_rates['avg_supplyRate_eth_rates'].tolist()
# print(supply_rate_list)

# Prices Data
filtered_data_prices = sorted_data_rates[['date_eth_volume', 'price_eth']]
eth_price_changes = filtered_data_prices['price_eth'].tolist()
# eth_price_changes = [1598.16, 1350, 2000, 1700, 1630, 1200, 1400] # example
# print(eth_price_changes)

num_days = len(eth_price_changes)

# Process of each day taking a new position
for start_day in range(num_days):
    liquidated_in_previous_loop = False
    leverage_level = []


    for loop in range(1, max_loop):

        # Reset values ​​at the start of each new position day
        total_eth_supplied = initial_eth_amount
        total_usdc_borrowed = 0
        eth_price = eth_price_changes[start_day]

        # Loan loop only on the first day of each new position
        for _ in range(loop):
            total_token_borrow_previous_loop = total_usdc_borrowed
            total_token_supply_previous_loop = total_eth_supplied

            usdc_borrowed = total_token_supply_previous_loop * eth_price * (1/max_ltv) - total_token_borrow_previous_loop
            total_usdc_borrowed = total_token_borrow_previous_loop + usdc_borrowed

            extra_eth_supplied = usdc_borrowed / eth_price
            total_eth_supplied = total_token_supply_previous_loop + extra_eth_supplied

            # Initial LTV
            total_supply_mkt_value = total_eth_supplied * eth_price
            ltv = total_usdc_borrowed / total_supply_mkt_value
            leverage_level.append(total_eth_supplied / initial_eth_amount)

            # Store the results of the first day of loans
            new_row = pd.DataFrame({
                'Start Day': [start_day],
                'Loop': [loop],
                'Day': [0],  # The first day is always 0
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

        # Simulation for the next 7 days
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

            # Store daily results
            new_row = pd.DataFrame({
                'Start Day': [start_day],
                'Loop': [loop],
                'Day': [day],  # Subsequent days
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
    
# Setting to show more rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)  # Ajustar el ancho de la pantalla

# Print the dataFrame and settled Times
print(results_df)
print("Times liquidated:", times_liquidated)
# Save the dataframe in a csv
results_df.to_csv('./results/looping_descriptive_model_results.csv', index=False)

# Create summary DataFrame for settlements
summary_df = pd.DataFrame(0, index=[f'Loop {i}' for i in range(1, max_loop)], columns=[f'Start Day {i}' for i in range(num_days)])

# Fill the summary DataFrame with the settlement data
for loop in range(1, max_loop):
    for start_day in range(num_days):
        # Check if there was any settlement in the series of 7 days following start_day
        liquidated = results_df[(results_df['Start Day'] == start_day) & (results_df['Loop'] == loop) & (results_df['Liquidated'])]['Liquidated'].any()
        summary_df.at[f'Loop {loop}', f'Start Day {start_day}'] = 1 if liquidated else 0

# Print the Summary DataFrame
print(summary_df)
summary_df.to_csv('./results/dummy_matrix.csv', index=False)

frequencies = summary_df.apply(lambda row: row.sum() / len(row), axis=1)
frequencies_df = pd.DataFrame(frequencies, columns=['Frequency'])
frequencies_df.index = [index.replace('Loop ', '') for index in frequencies_df.index]
leverage_level = sorted(list(set(leverage_level)))
frequencies_df['Leverage_Level'] = leverage_level
print(frequencies_df)

frequencies_df.to_csv('./results/frequencies_by_loop.csv', index=True, index_label='Loop Number')

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=frequencies_df.index, y='Frequency', data=frequencies_df, palette='coolwarm')

plt.title('Frequency of liquidation per Loop', fontsize=16, fontweight='bold')
plt.xlabel('Loop', fontsize=14, fontweight='bold')
plt.ylabel('Frequency', fontsize=14, fontweight='bold')

plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points')

plt.show()