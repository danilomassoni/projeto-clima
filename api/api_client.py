# Funções para conexão e manipulação da API pública

import pandas as pd
import requests


def fetch_weather_from_api(city):

    API_KEY = "0fa1f562bb59ce63b1023e10fc3416f7"
    city = "São Paulo"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt_br"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "cidade": data["name"],
            "temperatura": data["main"]["temp"],
            "umidade": data["main"]["humidity"],
            "descricao": data["weather"][0]["description"],
            "data_consulta": pd.Timestamp.now()
        }
    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None