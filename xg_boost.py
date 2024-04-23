import pandas as pd, numpy as np, xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report





# Asegúrate de que el DataFrame está ordenado por fecha
df = df.sort_values('date')

# Ejemplo de cómo podrías calcular algunas de las características derivadas
df['day_range'] = df['high_price'] - df['low_price']
df['day_price_change'] = df['adj_close'].diff()
df['day_volume_change'] = df['volume'].pct_change()  # Cambio porcentual del volumen respecto al día anterior
# Calcular las medias móviles de 14, 21 y 30 días para 'low_price'
df['moving_average_14_low'] = df['low_price'].rolling(window=7, min_periods=1).mean()
df['moving_average_14_low'] = df['low_price'].rolling(window=14, min_periods=1).mean()
df['moving_average_21_low'] = df['low_price'].rolling(window=21, min_periods=1).mean()
df['moving_average_30_low'] = df['low_price'].rolling(window=30, min_periods=1).mean()

# Asume que 'is_liquidated' es tu variable objetivo
X = df.drop(['is_liquidated'], axis=1)
y = df['is_liquidated']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import xgboost as xgb

model = xgb.XGBClassifier(
    objective='binary:logistic',
    colsample_bytree=0.4,
    learning_rate=0.1,
    max_depth=5,
    alpha=10,
    n_estimators=100
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)
print(f"Accuracy: {accuracy}")
print(confusion_matrix(y_test, preds))
print(classification_report(y_test, preds))
