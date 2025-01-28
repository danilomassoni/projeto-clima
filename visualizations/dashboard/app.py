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

# Carregar dados Históricos 
df_historico = pd.read_csv('data/processed/dataframe_formatado.csv', sep=';')
df_historico['ds'] = pd.to_datetime(df_historico['ano'].astype(str) + '-' + df_historico['mes'].astype(str) + '-01')
df_historico['y'] = df_historico['temperatura']

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

    html.Div([
        html.Label("Selecione o intervalo de anos:"),
        dcc.RangeSlider(
            id="year_range_slider",
            min=df_historico['ds'].dt.year.min(),
            max=df_historico['ds'].dt.year.max(),
            value=[df_historico['ds'].dt.year.min(), df_historico['ds'].dt.year.max()],
            marks={year: str(year) for year in range(df_historico['df'].dt.year.min(), df_historico['ds'].dt.year.max() + 1, 5)}
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Label("Exibir Dados:"),
        dcc.Checklist(
            id="data_selector",
            options=[
                {'label': 'Histórico', 'value': 'historico'},
                {'label': 'Previsão', 'value': 'previsao'}
            ],
            value=['historico', 'previsao'], # Mostrar os padrões
            inline=True
        )
    ], style={'margin': '20px'}),

    html.Div(id="error_message", style={'color': 'red', 'textAlign': 'center'}),
    dcc.Graph(id="forecast_graph")
])

# Callback para atualizar a previsão
@app.callback(
    [Output("forecast_graph", "figure"),
     Output("error_message", "children")],
    [Input("submit_button", 'n_clicks')],
    [
        dash.dependencies.State("years_input", "value"),
        dash.dependcies.State("year_range_slider", "value"),
        dash.dependencies.State("data_selector", "Value")
     ]
)
def update_forecast(n_clicks, years_to_predict, year_range, data_selector):
    try:
        if not years_to_predict or years_to_predict < 1:
            return {}, "Por favor, insira um número válido de anos."

        # Gerar a previsão
        forecast = generate_forecast(years_to_predict)

        # Filtrar dados históricos
        historico_filtrado = df_historico[
            (df_historico['ds'].dt.year >= year_range[0]) &
            (df_historico['ds'].dt.year <= year_range[1])
        ]

        # Filtrar previsao
        previsao_filtrada = forecast[
            (forecast['ds'].dt.year >= year_range[0]) &
            (forecast['ds'].dt.year <= year_range[1])
        ]

        # Dados para o gráfico
        data = []
        if 'historico' in data_selector:
            data.append(go.Scatter(
                x=historico_filtrado['ds'],
                y=historico_filtrado['y'],
                mode='lines',
                name='Historico',
                line=dict(color='gray')
            ))
        if 'previsao' in data_selector:
            data.append(go.Scatter(
                x=previsao_filtrada['ds'],
                y=historico_filtrado['y'],
                mode='lines',
                name='Historico',
                line=dict(color='gray')
            ))
            data.append(go.Scatter(
                x=previsao_filtrada['ds'],
                y=previsao_filtrada['yhat_lower'],
                mode='lines',
                name='Intervalo Inferior',
                line=dict(dash='dot', color='lightblue')
            ))

        if not data:
            return {}, "Nenhum dado disponível para os filtros aplicados."


        # Criar o gráfico com Plotly
        figure = {
            'data': data,
            'layout': go.Layout(
                title="Previsão de Temperatura",
                xaxis="Previsão de Temperatura",
                yaxis=dict(title="Temperatura (ºC)"),
                hovermode="cloest"
            )
        }

        return figure, ""
    except Exception as e:
        return {}, f"Erro ao gerar a previsão: {e}"

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True) # Padrão para acesso: http://127.0.0.1:8050
