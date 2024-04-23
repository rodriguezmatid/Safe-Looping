import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm

df = pd.read_csv('datasets/final_combined_dataset.csv')

# Lista todas las columnas en el DataFrame
list_of_columns = df.columns.tolist()
# print("Las columnas en el DataFrame son:")
# print(list_of_columns)

# nan_columns = df.isna().any()
# print(nan_columns)

# Descartar los primeros 7 días
df_cleaned = df[7:].reset_index(drop=True)

# Eliminar la columna de fecha ya que no la utilizarás en la regresión
df_cleaned.drop(['date_eth_volume'], axis=1, inplace=True)

# Definir las características (X) y la variable objetivo (y)
# X = df_cleaned.drop('weekly_change_eth', axis=1)  # Incluye todas las variables excepto la variable objetivo # 1
# X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume']] # 2
# X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume', 'moving_average_7_price_eth', 'moving_average_14_price_eth', 'moving_average_21_price_eth', 'moving_average_30_price_eth', 'moving_average_7_volume_eth', 'moving_average_14_volume_eth', 'moving_average_21_volume_eth', 'moving_average_30_volume_eth', 'moving_average_7_mc_eth', 'moving_average_14_mc_eth', 'moving_average_21_mc_eth', 'moving_average_30_mc_eth']] # 3
# X = df_cleaned[['deposits_volume_v3_eth_daily_deposits_borrows', 'borrows_volume_v3_eth_daily_deposits_borrows', 'deposits_volume_v3_usdc_daily_deposits_borrows', 'borrows_volume_v3_usdc_daily_deposits_borrows']] # 4
# X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume', 'deposits_volume_v3_eth_daily_deposits_borrows', 'borrows_volume_v3_eth_daily_deposits_borrows', 'deposits_volume_v3_usdc_daily_deposits_borrows', 'borrows_volume_v3_usdc_daily_deposits_borrows']] # 5
# X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume', 'deposits_volume_v3_eth_daily_deposits_borrows', 'borrows_volume_v3_eth_daily_deposits_borrows', 'deposits_volume_v3_usdc_daily_deposits_borrows', 'borrows_volume_v3_usdc_daily_deposits_borrows', 'moving_average_7_price_eth', 'moving_average_14_price_eth', 'moving_average_21_price_eth', 'moving_average_30_price_eth', 'moving_average_7_volume_eth', 'moving_average_14_volume_eth', 'moving_average_21_volume_eth', 'moving_average_30_volume_eth', 'moving_average_7_mc_eth', 'moving_average_14_mc_eth', 'moving_average_21_mc_eth', 'moving_average_30_mc_eth', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_7', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_14', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_21', 'deposits_volume_v3_eth_daily_deposits_borrows_ma_30', 'borrows_volume_v3_eth_daily_deposits_borrows_ma_7', 'borrows_volume_v3_eth_daily_deposits_borrows_ma_14', 'borrows_volume_v3_eth_daily_deposits_borrows_ma_21', 'borrows_volume_v3_eth_daily_deposits_borrows_ma_30', 'deposits_volume_v3_usdc_daily_deposits_borrows_ma_7', 'deposits_volume_v3_usdc_daily_deposits_borrows_ma_14', 'deposits_volume_v3_usdc_daily_deposits_borrows_ma_21', 'deposits_volume_v3_usdc_daily_deposits_borrows_ma_30', 'borrows_volume_v3_usdc_daily_deposits_borrows_ma_7', 'borrows_volume_v3_usdc_daily_deposits_borrows_ma_14', 'borrows_volume_v3_usdc_daily_deposits_borrows_ma_21', 'borrows_volume_v3_usdc_daily_deposits_borrows_ma_30']] # 6
# X = df_cleaned[['avg_stableBorrowRate_eth_rates', 'avg_variableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'avg_liquidityIndex_eth_rates', 'avg_variableBorrowIndex_eth_rates', 'avg_stableBorrowRate_usdc_rates', 'avg_variableBorrowRate_usdc_rates', 'avg_supplyRate_usdc_rates', 'avg_liquidityIndex_usdc_rates', 'avg_variableBorrowIndex_usdc_rates']] # 7
# X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume', 'avg_stableBorrowRate_eth_rates', 'avg_variableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'avg_liquidityIndex_eth_rates', 'avg_variableBorrowIndex_eth_rates', 'avg_stableBorrowRate_usdc_rates', 'avg_variableBorrowRate_usdc_rates', 'avg_supplyRate_usdc_rates', 'avg_liquidityIndex_usdc_rates', 'avg_variableBorrowIndex_usdc_rates']] # 8
X = df_cleaned[['price_eth', 'market_cap_eth_volume', 'volumes_last_24h_eth_volume', 'avg_stableBorrowRate_eth_rates', 'avg_variableBorrowRate_eth_rates', 'avg_supplyRate_eth_rates', 'avg_liquidityIndex_eth_rates', 'avg_variableBorrowIndex_eth_rates', 'avg_stableBorrowRate_usdc_rates', 'avg_variableBorrowRate_usdc_rates', 'avg_supplyRate_usdc_rates', 'avg_liquidityIndex_usdc_rates', 'avg_variableBorrowIndex_usdc_rates', 'moving_average_7_price_eth', 'moving_average_14_price_eth', 'moving_average_21_price_eth', 'moving_average_30_price_eth', 'moving_average_7_volume_eth', 'moving_average_14_volume_eth', 'moving_average_21_volume_eth', 'moving_average_30_volume_eth', 'moving_average_7_mc_eth', 'moving_average_14_mc_eth', 'moving_average_21_mc_eth', 'moving_average_30_mc_eth', 'avg_stableBorrowRate_eth_rates_ma_7', 'avg_stableBorrowRate_eth_rates_ma_14', 'avg_stableBorrowRate_eth_rates_ma_21', 'avg_stableBorrowRate_eth_rates_ma_30', 'avg_variableBorrowRate_eth_rates_ma_7', 'avg_variableBorrowRate_eth_rates_ma_14', 'avg_variableBorrowRate_eth_rates_ma_21', 'avg_variableBorrowRate_eth_rates_ma_30', 'avg_supplyRate_eth_rates_ma_7', 'avg_supplyRate_eth_rates_ma_14', 'avg_supplyRate_eth_rates_ma_21', 'avg_supplyRate_eth_rates_ma_30', 'avg_liquidityIndex_eth_rates_ma_7', 'avg_liquidityIndex_eth_rates_ma_14', 'avg_liquidityIndex_eth_rates_ma_21', 'avg_liquidityIndex_eth_rates_ma_30', 'avg_variableBorrowIndex_eth_rates_ma_7', 'avg_variableBorrowIndex_eth_rates_ma_14', 'avg_variableBorrowIndex_eth_rates_ma_21', 'avg_variableBorrowIndex_eth_rates_ma_30']] # 9

y = df_cleaned['weekly_change_eth']  # Variable objetivo
X = sm.add_constant(X)

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Crear y entrenar el modelo de regresión lineal
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Realizar predicciones en el conjunto de prueba
# y_pred = model.predict(X_test)

# # Evaluar el modelo
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# # Preparar datos para guardar
# results = {
#     'Metric': ['MSE', 'R-squared'] + [f'Coefficient ({col})' for col in X.columns],
#     'Value': [mse, r2] + list(model.coef_)
# }

# # Crear DataFrame
# results_df = pd.DataFrame(results)

# # Guardar los resultados en un CSV
# results_df.to_csv('datasets/model_results_and_coefficients.csv', index=False)

# print("Mean Squared Error (MSE):", mse)
# print("R-squared (R2):", r2)

# # Opcional: Mostrar los coeficientes del modelo
# print("Coeficientes del modelo:")
# for feature, coef in zip(X.columns, model.coef_):
#     print(f"{feature}: {coef}")


#### Second Model
model = sm.OLS(y_train, X_train)
results = model.fit()

# Realizar predicciones en el conjunto de prueba
y_pred = results.predict(X_test)

# Calcular MSE y R2
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Preparar datos para guardar
results_data = {
    'Metric': ['MSE', 'R-squared'] + [f'Coefficient ({col})' for col in X.columns if col != 'const'],
    'Value': [mse, r2] + list(results.params.values)[1:],
    'P-value': ['NA', 'NA'] + list(results.pvalues.values)[1:],
    'Low CI 95%': ['NA', 'NA'] + list(results.conf_int(alpha=0.05).iloc[1:, 0]),
    'High CI 95%': ['NA', 'NA'] + list(results.conf_int(alpha=0.05).iloc[1:, 1])
}

results_df = pd.DataFrame(results_data)

# Guardar los resultados en un CSV
results_df.to_csv('datasets/model_9.csv', index=False)

print("Mean Squared Error (MSE):", mse)
print("R-squared (R2):", r2)
print("Model details saved to 'complete_model_results.csv'")