import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        """Carrega os dados históricos do arquivo CSV."""
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Carrega e processa os dados do CSV."""
        self.df = pd.read_csv(self.file_path, sep=';')

        # Criar dicionário de mapeamento de meses
        meses_map = {
            "JAN.": 1, "FEV.": 2, "MAR.": 3, "ABR.": 4, "MAI.": 5, "JUN.": 6,
            "JUL.": 7, "AGO.": 8, "SET.": 9, "OUT.": 10, "NOV.": 11, "DEZ.": 12
        }

        # Converter os meses para números
        self.df['mes'] = self.df['mes'].str.strip().replace(meses_map).astype(int)

        # Criar a coluna de datas corretamente
        self.df['ds'] = pd.to_datetime(self.df['ano'].astype(str) + '-' + self.df['mes'].astype(str) + '-01', format='%Y-%m-%d')
        self.df['y'] = self.df['temperatura']

        return self.df
