import requests
import mysql.connector
import time
from datetime import datetime
import csv
import getpass
from pathlib import Path
import schedule
import arrow

data_atual = datetime.now() # Obtém a data atual
data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
data_formatada = int(data_string) # converte em INT
api_key = '' # Substitua 'YOUR_API_KEY' pela sua chave da API OpenWeatherMap
city_name = 'sao paulo' # Substitua 'YOUR_CITY_NAME' pelo nome da sua cidade

# coletar informações no banco de dados
get_query = '''
    SELECT data, temperatura, umidade, descricao  
    FROM previsao
'''

# Inserir informações no banco de dados
insert_query = '''
    INSERT INTO previsao (data, temperatura, umidade, descricao)
    VALUES (%s, %s, %s, %s)
'''

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


def hours():
    # Configura o fuso horário para Brasília
    tz_brasil = 'America/Sao_Paulo'
    
    # Obtém a hora atual com o fuso horário de Brasília
    hora_atual_brasil = arrow.now(tz_brasil)
    
    # Formata a hora no padrão desejado (HH:MM)
    hora_formatada = hora_atual_brasil.format('HHmm')
    
    return hora_formatada

#Função que coleta o nome do usuario logado na maquina
def get_username():
    return getpass.getuser()

#Cria o arquivo .csv para salvar as informações do banco
def create_log_file():
    hours_current = hours()
    name_user = get_username()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\Backup\\{data_string}_Dados_Banco_Previsao_{hours_current}.csv"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\Backup")
    path.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as arquivo:
        pass
    return log_file

#obtem todos as informações salvas na planilha previsao e salva em um csv
def backup():
        cursor.execute(get_query)
        result = cursor.fetchall()
        backup = create_log_file()

        with open(backup, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Data', 'Temperatura', 'Umidade', 'Descrição'])  # Escreve o cabeçalho

            for row in result:
                data, temperatura, umidade, descricao = row
                csvwriter.writerow([data, temperatura, umidade, descricao])

        print("Dados salvos no arquivo CSV")

#Coleta os dados da API
def collect_data():
    # URL da API OpenWeatherMap
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=pt_br&units=metric&appid={api_key}'

    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        temperatura = data['main']['temp']
        umidade = data['main']['humidity']
        descricao = data['weather'][0]['description']

        values = (data_formatada, temperatura, umidade, descricao)
        cursor.execute(insert_query, values)
        conn.commit()
        print("Dados inseridos no banco de dados")

    else:
        print("Erro ao obter dados da API")

    

# Agendar a coleta de dados da API a cada 10 minutos
schedule.every(10).minutes.do(collect_data)

# Agendar a função backup() a cada 10 horas
schedule.every(10).hours.do(backup)

while True:
    schedule.run_pending()
    time.sleep(1)


# Fechar a conexão com o banco de dados ao final
conn.close()

