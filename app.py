# Arquivo principal para rodar o projet
import dash 
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go 
from src.data_loader import DataLoader 
from src.model import ClimateModel

app = dash.Dash(__name__)
app.title = "Previsão Climática - São Paulo"

# Carregar os dados históricos usando a classe DataLoader
data_loader = DataLoader('data\processed\dataframe_formatado.csv')
df_historico = data_loader.load_data()


# Layout da Dashboard
app.layout = html.Div([
    html.H1("Previsão do Clima em São Paulo", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Quantos anos deseja prever?"),
        dcc.Input(id="yaers_input", type="number", value=5, min=1, max=20, step=1),
        html.Button("Atualizar Previsão", id="submit_button", n_clicks=0)
    ], style={'margin': '20px'}),

    dcc.Graph(id="forecast_graph")
])

#Callback para atualizar a previsão
@app.callback(
    Output("forecast_graph", "figure"),
    Input("submit_button", 'n_clicks'),
    Input("years_input", "value")
)

def update_forecast(n_clicks, years_to_predict):
    if not years_to_predict or years_to_predict < 1:
        return {}

    # Criar e treinar o modelo
    climate_model = ClimateModel(df_historico)
    climate_model.train()
    forecast = climate_model.forecast(years_to_predict)

    # Criar gráfico
    data = [
        go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Previsão'),
        go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Limite Inferior', line=dict(dash='dot')),
        go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Limite Superior', line=dict(dash='dot'))
    ]

    return {'data': data, 'layout': go.Layout(title="PRevisão de temperatura", xaxix_title="Ano", yaxis_title="Temperatura (ºC)")}


# Rodar o servidor 
if __name__ == "__main__":
    app.run_server(debug=True) # http://127.0.0.1:8050/