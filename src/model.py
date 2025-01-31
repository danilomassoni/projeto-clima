# Classe para treinar o modelo Prophet e gerar previsões

from prophet import Prophet
import pandas as pd

class ClimateModel:
    def __init__(self, data):
        self.data = data
        self.model = Prophet()

    def train(self):
        self.model.fit(self.data)

    def forecast(self, years):
        future = self.model.make_future_dataframe(periods=years * 12, freq='M')
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
