# Funções para criar gráficos e visualizações

import matplotlib.pyplot as plt

def plot_real_vs_predicted(y_real, y_pred):
    # Plota os valores reais e os previstos.

    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(y_real)), y_real, color="blue", label="Real")
    plt.scatter(range(len(y_pred)), y_pred, color="red", label="Previsto")
    plt.title("Valores reais (azul) vs. Previstos (vermelho)")
    plt.xlabel("Índice")
    plt.ylabel("valor")
    plt.ylabel("Temperatura")
    plt.legend()
    plt.grid(True)
    plt.show()