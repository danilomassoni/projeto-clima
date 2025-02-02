# Arquivo principal para rodar o projet
import dash 
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go 
from src.data_loader import DataLoader 
from src.model import ClimateModel
from src.database import Database

app = dash.Dash(__name__)
app.title = "Previsão Climática - São Paulo"

# Inicializar conexão com o banco e criar a tabela
db = Database()
db.create_table()

# Carregar os dados históricos usando a classe DataLoader
data_loader = DataLoader(r'data\processed\dataframe_formatado.csv')
df_historico = data_loader.load_data()




# Layout da Dashboard
app.layout = html.Div([
    html.H1("Previsão do Clima em São Paulo", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Quantos anos deseja prever?"),
        dcc.Input(id="years_input", type="number", value=5, min=1, max=50, step=1),
        html.Button("Atualizar Previsão", id="submit_button", n_clicks=0)
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("Selecione os dados a exibir:"),
        dcc.Checklist(
            id="data_selector",
            options=[
                {'label': 'Dados Reais', 'value': 'real'},
                {'label': 'Previsão', 'value': 'forecast'},
                {'label': 'Intervalo de Confiança', 'value': 'confidence'}
            ],
            value=['real', 'forecast', 'confidence'],  # Exibir todos por padrão
            inline=True
        )
    ], style={'margin': '20px'}),

    dcc.Graph(id="forecast_graph")
])


#Callback para atualizar a previsão
@app.callback(
    Output("forecast_graph", "figure"),
    [Input("submit_button", 'n_clicks'),
    Input("years_input", "value"),
    Input("data_selector", "value")]
)

def update_forecast(n_clicks, years_to_predict, data_selector):
    if not years_to_predict or years_to_predict < 1:
        return {'data': [], 'layout': go.Layout(title="Previsão de Temperatura", xaxis_title="Ano", yaxis_title="Temperatura (ºC)")}

    # Criar e treinar o modelo
    climate_model = ClimateModel(df_historico)
    climate_model.train()
    forecast = climate_model.forecast(years_to_predict)

    # Criar gráfico
    data = []
    if 'real' in data_selector:
        data.append(go.Scatter(x=df_historico['ds'], y=df_historico['y'], mode='lines+markers', name='Dados Reais', line=dict(color='gray')))

    if 'forecast' in data_selector:
        data.append(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Previsão', line=dict(color='blue')))

    if 'confidence' in data_selector:
        data.append(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Limite Inferior', line=dict(dash='dot', color='lightblue')))
        data.append(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Limite Superior', line=dict(dash='dot', color='lightblue')))

    return {'data': data, 'layout': go.Layout(title="Previsão de Temperatura", xaxis_title="Ano", yaxis_title="Temperatura (ºC)")}



# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True) # http://127.0.0.1:8050/