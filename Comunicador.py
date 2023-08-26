import requests
import mysql.connector
import time
from datetime import datetime
import csv
import getpass
from pathlib import Path
import schedule
import arrow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

data_atual = datetime.now() # Obtém a data atual
data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
data_formatada = int(data_string) # converte em INT
api_key = '' # Substitua 'YOUR_API_KEY' pela sua chave da API OpenWeatherMap
city_name = 'sao paulo' # Substitua 'YOUR_CITY_NAME' pelo nome da sua cidade

# coletar informações no banco de dados
get_query = '''
    SELECT data, temperatura, umidade, descricao, hora  
    FROM previsao
'''

# Inserir informações no banco de dados
insert_query = '''
    INSERT INTO previsao (data, temperatura, umidade, descricao, hora)
    VALUES (%s, %s, %s, %s, %s)
'''

# Conectar ao banco de dados MySQL (db4free.net)
conn = mysql.connector.connect(
    host='85.10.205.173', # Substitua pelo endereço IP ou nome do host do seu servidor MySQL
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
        descricao TEXT,
        hora INT
               
    )
''')
conn.commit()

def send_email(file_path):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Credenciais de login no Gmail
    email_username = 'tomate.irrigacao@gmail.com'
    email_password = ''
    email_client = '' #e-mail que receberá o arquivo

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = email_client 
    msg['Subject'] = 'Arquivo CSV de Previsão'

    body = "Segue anexo o arquivo CSV de previsão."
    msg.attach(MIMEText(body, 'plain'))

    with open(file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype="csv")
        attachment.add_header('content-disposition', 'attachment', filename=file_path)
        msg.attach(attachment)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(email_username, email_client, msg.as_string())
    server.quit()


def hours():
    # Configura o fuso horário para Brasília
    tz_brasil = 'America/Sao_Paulo'
    
    # Obtém a hora atual com o fuso horário de Brasília
    hora_atual_brasil = arrow.now(tz_brasil)
    
    # Formata a hora no padrão desejado (HH:MM)
    hora_formatada =int(hora_atual_brasil.format('HHmm'))
    
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
            csvwriter.writerow(['Data', 'Temperatura', 'Umidade', 'Descrição', 'hora'])  # Escreve o cabeçalho

            for row in result:
                data, temperatura, umidade, descricao, hora = row
                csvwriter.writerow([data, temperatura, umidade, descricao, hora])

        send_email(backup)
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
        hours_current = hours()

        values = (data_formatada, temperatura, umidade, descricao, hours_current)
        cursor.execute(insert_query, values)
        conn.commit()
        print("Dados inseridos no banco de dados")

    else:
        print("Erro ao obter dados da API")

    

# Agendar a coleta de dados da API a cada 10 minutos
schedule.every(10).minutes.do(collect_data)

# Agendar a função backup() a cada 10 horas
schedule.every(10).seconds.do(backup)

while True:
    schedule.run_pending()
    time.sleep(1)


# Fechar a conexão com o banco de dados ao final
conn.close()

