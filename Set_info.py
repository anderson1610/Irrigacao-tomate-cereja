import requests
import mysql.connector
import time
from datetime import datetime

# Obtém a data atual
data_atual = datetime.now()

# Formata a data no padrão brasileiro (dd/mm/aaaa)
data_string = data_atual.strftime('%d%m%Y')
data_formatada = int(data_string)


# Substitua 'YOUR_API_KEY' pela sua chave da API OpenWeatherMap
api_key = ''

# Substitua 'YOUR_CITY_NAME' pelo nome da sua cidade
city_name = 'sao paulo'

# Conectar ao banco de dados MySQL (db4free.net)
conn = mysql.connector.connect(
    host='', # Substitua pelo endereço IP ou nome do host do seu servidor MySQL
    user='',   # Substitua pelo nome de usuário do MySQL
    password='', # Substitua pela senha do MySQL
    database=''  # Substitua pelo nome do banco de dados
)
cursor = conn.cursor()

# Criar a tabela se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS previsao (
        data INT,      
        temperatura INT,
        umidade INT,
        descricao TEXT
    )
''')
conn.commit()

while True:
    # URL da API OpenWeatherMap
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=pt_br&units=metric&appid={api_key}'

    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        temperatura = data['main']['temp']
        umidade = data['main']['humidity']
        descricao = data['weather'][0]['description']

        # Inserir informações no banco de dados
        insert_query = '''
            INSERT INTO previsao (data, temperatura, umidade, descricao)
            VALUES (%s, %s, %s, %s)
        '''
        values = (data_formatada, temperatura, umidade, descricao)
        cursor.execute(insert_query, values)
        conn.commit()

        print("Dados inseridos no banco de dados")

    else:
        print("Erro ao obter dados da API")

    time.sleep(6000) 

# Fechar a conexão com o banco de dados ao final
conn.close()
