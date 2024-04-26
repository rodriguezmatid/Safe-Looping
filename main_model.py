import pandas as pd, functions, numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.width', 1000) 

liquidation_cost = 0.05

df = pd.read_csv('./results/final_combined_dataset.csv')

# # Some data engineering #
selected_columns = ['avg_stableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'price_eth', 'deposits_volume_v3_eth_daily_deposits_borrows', 'borrows_volume_v3_eth_daily_deposits_borrows']

# print(df[selected_columns].head())

# print(df[selected_columns].describe())

# # Individual Histograms
# for column in selected_columns:
#     df[column].hist()
#     plt.title(f'Histogram of {column}')
#     plt.xlabel(column)
#     plt.ylabel('Frequency')
#     plt.show()

# # All the histograms
# df[selected_columns].hist(figsize=(12, 8))
# plt.tight_layout()
# plt.show()

# # Heatmap of correlations for selected columns
# plt.figure(figsize=(10, 8))
# sns.heatmap(df[selected_columns].corr(), annot=True, fmt=".2f", cmap='coolwarm')
# plt.title("Heatmap of Correlations Among Selected Columns")
# plt.show()

# List all columns in the DataFrame
list_of_columns = df.columns.tolist()
print("The columns for the dataframe:")
print(list_of_columns)

# Discard the first 7 days to have a good format in the db
df_cleaned = df[7:].reset_index(drop=True)

# Delete the date column since won't be useful in the 7 day regression
df_cleaned.drop(['date_eth_volume'], axis=1, inplace=True)

df_selected = df_cleaned[selected_columns]

df_selected = df_selected.dropna()

# # Calculating the Covariance Matrix
# covariance_matrix = df_selected.cov()
# print("Covariance Matrix:")
# print(covariance_matrix)

X = df_cleaned[['avg_stableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'weekly_change_usdc', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_21', 'price_eth', 'moving_average_14_price_eth', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_14', 'moving_average_21_price_eth', 'avg_stableBorrowRate_eth_rates_ma_7', 'avg_supplyRate_eth_rates_ma_7']] # 15

y = df_cleaned['weekly_change_eth']  # Target variable

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculation of MSE and R2
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

# Save model coefficients
coefficients = model.coef_
intercept = model.intercept_

print("Intercept:", intercept)
print("Coefficients:", coefficients)
features = ['avg_stableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'weekly_change_usdc', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_21', 'price_eth', 'moving_average_14_price_eth', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_14', 'moving_average_21_price_eth', 'avg_stableBorrowRate_eth_rates_ma_7', 'avg_supplyRate_eth_rates_ma_7']

# Create a dictionary to store the coefficients
coef_dict = {feature: coef for feature, coef in zip(features, coefficients)}
coef_dict['intercept'] = intercept

avg_stableBorrowRate_eth_rates_coef = coef_dict['avg_stableBorrowRate_eth_rates']
avg_supplyRate_eth_rates_coef = coef_dict['avg_supplyRate_eth_rates']
weekly_change_usdc_coef = coef_dict['weekly_change_usdc']
deposits_volume_v3_eth_daily_deposits_borrows_ma_21_coef = coef_dict['deposits_volume_v3_eth_daily_deposits_borrows_ma_21']
price_eth_coef = coef_dict['price_eth']
moving_average_14_price_eth_coef = coef_dict['moving_average_14_price_eth']
deposits_volume_v3_eth_daily_deposits_borrows_ma_14_coef = coef_dict['deposits_volume_v3_eth_daily_deposits_borrows_ma_14']
moving_average_21_price_eth_coef = coef_dict['moving_average_21_price_eth']
avg_stableBorrowRate_eth_rates_ma_7_coef = coef_dict['avg_stableBorrowRate_eth_rates_ma_7']
avg_supplyRate_eth_rates_ma_7_coef = coef_dict['avg_supplyRate_eth_rates_ma_7']

df_cleaned['estimated_weekly_price_change'] = df_cleaned.apply(lambda row: functions.calculate_estimated_change(row, coef_dict), axis=1)

df_cleaned['difference_in_estimation'] = df_cleaned['estimated_weekly_price_change'] - df_cleaned['weekly_change_eth']

# Saving filtered_df to a CSV
df_cleaned.to_csv('./results/dataset_with_prediction.csv', index=False)

# Plotting the difference between the estimation and the real change price
plt.figure(figsize=(12, 6)) # Set the size of the plot
plt.plot(df_cleaned.index, df_cleaned['estimated_weekly_price_change'], label='Estimated Weekly Price Change', color='blue') # Plot the line for estimated_weekly_price_change
plt.plot(df_cleaned.index, df_cleaned['weekly_change_eth'], label='Actual Weekly Change', color='red') # Plot the line for weekly_change_eth
plt.plot(df_cleaned.index, df_cleaned['difference_in_estimation'], label='Difference', color='green', linestyle='--') # Plot the line for the difference
plt.legend()
plt.title('Comparison of Estimated and Actual Weekly Price Changes')
plt.xlabel('Index')
plt.ylabel('Change')
plt.savefig('./images/comparison_plot.png') # Save the plot as a PNG file
plt.show() # Display the plot

# # Define the initial types for the ONNX model
# initial_type = [('float_input', FloatTensorType([None, len(features)]))]

# # Convert the scikit-learn model to ONNX
# onnx_model = convert_sklearn(model, initial_types=initial_type)

# # Save the ONNX model to a file
# with open("linear_regression.onnx", "wb") as f:
#     f.write(onnx_model.SerializeToString())

# Expected Return Model

# Combination with loop frequency
df_liquidation_frequency = pd.read_csv('./results/frequencies_by_loop.csv')

expected_returns = []
leverage_levels = []

# Bucle para iterar sobre las filas y calcular los retornos esperados
for index, row in df_liquidation_frequency.iterrows():
    frequency_liq = row['Frequency']
    leverage_level = row['Leverage_Level']
    
    # Guardar el nivel de apalancamiento en la lista
    leverage_levels.append(leverage_level)
    
    # Cálculo del expected_return para la combinación actual
    expected_return = (1 - frequency_liq) * y_pred * leverage_level - frequency_liq * liquidation_cost * leverage_level
    
    # Agregar el resultado a la lista
    expected_returns.append(expected_return)

# # Saving the y_pred
# y_pred_df = pd.DataFrame(y_pred, columns=['y_pred'])
# y_pred_df.to_csv('./results/y_pred.csv', index=False)

# # Saving the expected returns
# expected_returns_df = pd.DataFrame(expected_returns).T
# expected_returns_df.columns = [f'Leverage_Level_{level}' for level in leverage_levels]
# expected_returns_df.to_csv('./results/expected_returns.csv', index=False)

# Seaborn Style Settings
sns.set_theme(context='notebook', style='whitegrid')

# Generar una paleta de colores con Seaborn
palette = sns.color_palette("coolwarm", len(leverage_levels))

fig, ax = plt.subplots(figsize=(10, 6))

# Iterate over leverage levels and calculate expected returns for each prediction
for idx, leverage_level in enumerate(leverage_levels):
    expected_returns = (1 - frequency_liq) * y_pred * leverage_level - frequency_liq * liquidation_cost * leverage_level
    sns.lineplot(x=y_pred, y=expected_returns, label=f'Leverage Level {leverage_level}', color=palette[idx], ax=ax)

ax.set_xlabel('Predicted Weekly Change (y_pred)')
ax.set_ylabel('Expected Returns')
ax.set_title('Expected Returns vs. Predicted Weekly Change for Different Leverage Levels')
ax.legend(title='Leverage Levels')
plt.savefig('./images/expected_returns_plot.png')
plt.show()