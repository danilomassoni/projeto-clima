# Código para treinar e avaliar modelos preditivos
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
def train_regression_model(df):
    # Treina um modelo de regressão linear

    X = df[['umidade', 'dia_do_ano']] # Variáveis preditoras
    y = df['temperatura'] # Variável alvo

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    score = modelo.score(X_test, y_test) # Retorna o desempenho do modelo
    return modelo, score