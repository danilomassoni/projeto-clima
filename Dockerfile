# Imagem base do Python 3.9
FROM python:3.9

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . .

# Instalar as dependências do Python
RUN pip install --upgrade pip && pip install -r requiriments.txt

# A porta onde roda (8050)
EXPOSE 8050

# Definir o comando padrão para iniciar a aplicação
CMD ["python", "app.py"]