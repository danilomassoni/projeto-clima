# Script para a Dashboard

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from forecast_model import generate_forecast

# Inicializar o app Dash
app = dash.Dash(__name__)
app.title = "Previsão Climática - São Paulo"

# Layout da Dashboard
app.layout = html.Div([
    html.H1("Previsão do Clima em São Paulo", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Quantos anos deseja prever?"),
        dcc.Input(
            id="years_input",
            type="number",
            value=5,  # Valor padrão
            min=1,
            max=20,
            step=1,
            placeholder="Digite o número de anos"
        ),
        html.Button("Atualizar Previsão", id="submit_button", n_clicks=0),
    ], style={'margin': '20px'}),
    html.Div(id="error_message", style={'color': 'red', 'textAlign': 'center'}),
    dcc.Graph(id="forecast_graph")
])

# Callback para atualizar a previsão
@app.callback(
    [Output("forecast_graph", "figure"),
     Output("error_message", "children")],
    [Input("submit_button", 'n_clicks')],
    [dash.dependencies.State("years_input", "value")]
)
def update_forecast(n_clicks, years_to_predict):
    try:
        if not years_to_predict or years_to_predict < 1:
            return {}, "Por favor, insira um número válido de anos."

        # Gerar a previsão
        forecast = generate_forecast(years_to_predict)

        # Criar o gráfico com Plotly
        figure = {
            'data': [
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    mode='lines',
                    name='Previsão',
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    mode='lines',
                    name='Intervalo Superior',
                    line=dict(dash='dot', color='lightblue')
                ),
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    mode='lines',
                    name='Intervalo Inferior',
                    line=dict(dash='dot', color='lightblue')
                )
            ],
            'layout': go.Layout(
                title="Previsão de Temperatura",
                xaxis=dict(title="Data"),
                yaxis=dict(title="Temperatura (ºC)"),
                hovermode="closest"
            )
        }

        return figure, ""
    except Exception as e:
        return {}, f"Erro ao gerar a previsão: {e}"

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True) # Padrão para acesso: http://127.0.0.1:8050
