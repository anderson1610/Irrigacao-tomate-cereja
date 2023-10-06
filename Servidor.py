import mysql.connector
import time
from datetime import datetime
import csv
import requests
import getpass
from pathlib import Path
import schedule
import arrow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import markov

data_atual = datetime.now() # Obtém a data atual
data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
data_formatada = int(data_string) # converte em INT
api_key = '' # Substitua 'YOUR_API_KEY' pela sua chave da API OpenWeatherMap
city_name = 'São Paulo' # Substitua 'YOUR_CITY_NAME' pelo nome da sua cidade
weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=pt_br&units=metric&appid={api_key}' # URL da API OpenWeatherMap

# Credenciais de login no Gmail
email_username = 'tomate.irrigacao@gmail.com' 
email_password = ''
email_client = 'anderson.camargo1@aluno.unip.br' #e-mail que receberá o arquivo

# Conectar ao banco de dados MySQL (db4free.net)
conn = mysql.connector.connect(
    host='85.10.205.173', # Substitua pelo endereço IP ou nome do host do seu servidor MySQL
    user='',   # Substitua pelo nome de usuário do MySQL
    password='', # Substitua pela senha do MySQL
    database='tccarduino2023'  # Substitua pelo nome do banco de dados
)

cursor = conn.cursor()

# Criar a tabela se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS previsao (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        data INT,      
        temperatura INT,
        umidade INT,
        descricao TEXT,
        hora INT
               
    )
''')
conn.commit()

# coletar informações no banco de dados de previsao
get_query = '''
    SELECT data, temperatura, umidade, descricao, hora  
    FROM previsao
'''

#Coletar informações do consumo de agua do banco
get_query_water = '''
    SELECT Data, Gasto   
    FROM CustoAgua
'''

# Inserir informações no banco de dados de previsao
insert_query = '''
    INSERT INTO previsao (data, temperatura, umidade, descricao, hora)
    VALUES (%s, %s, %s, %s, %s)
'''

#função para envio de e-mail backup do banco com as informações do tempo
def send_email_backup(file_path):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

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
    print('Email de backup enviado!')
    
#Coleta o horario atual em tipo inteiro
def hours():
    # Configura o fuso horário para Brasília
    tz_brasil = 'America/Sao_Paulo'
    
    # Obtém a hora atual com o fuso horário de Brasília
    hora_atual_brasil = arrow.now(tz_brasil)
    
    # Formata a hora no padrão desejado (HH:MM)
    hora_formatada =int(hora_atual_brasil.format('HHmm'))
    
    return hora_formatada

#Coleta o hoario atual em tipo string
def hours_default():
    # Configura o fuso horário para Brasília
    tz_brasil = 'America/Sao_Paulo'
    
    # Obtém a hora atual com o fuso horário de Brasília
    hora_atual_brasil = arrow.now(tz_brasil)
    
    # Formata a hora no padrão desejado (HH:MM)
    hora_formatada =hora_atual_brasil.format('HH:mm')
    
    return hora_formatada


#Função que coleta o nome do usuario logado na maquina
def get_username():
    return getpass.getuser()

#Cria o arquivo .csv para salvar as informações do banco previsao
def create_log_file():
    data_atual = datetime.now() # Obtém a data atual
    data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
    data_formatada = int(data_string) # converte em INT
    hours_current = hours()
    name_user = get_username()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\Backup\\{data_string}_Dados_Banco_Previsao_{hours_current}.csv"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\Backup")
    path.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as arquivo:
        pass
    return log_file

#obtem todos as informações salvas no banco previsao e salva em um csv
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

        send_email_backup(backup)
        print("Dados de backup salvos no arquivo CSV")
        

#Coleta os dados da API e envia ao banco de dados
def collect_data():

    data_atual = datetime.now() # Obtém a data atual
    data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
    data_formatada = int(data_string) # converte em INT
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
        print("Dados referente a API inseridos no banco de dados")
        return f'Temperatura: {temperatura} | Umidade: {umidade} | {city_name}: {descricao}'
    else:
        print("Erro ao obter dados da API")

#Atualiza as informações da previsão na interface
def info_interface():
    response = requests.get(weather_url)
    data = response.json()
    
    if response.status_code == 200:
        temperatura = data['main']['temp']
        descricao = data['weather'][0]['description']
        descricao_m = descricao.capitalize()
        Estado = city_name.upper()
        hours_current = hours_default()
        return f'{Estado} | Temperatura: {temperatura} {descricao_m} | Horário: {hours_current}'
    else:
        print("Erro ao obter dados da API")   
        

#função para envio de e-mail com as informações do gasto de água
def send_email_water(file_path, consumption):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = email_client 
    msg['Subject'] = 'Arquivo CSV do fluxo/gasto de água'

    body = f"Segue anexo o arquivo CSV de gasto de água. Consumo de: {consumption}"
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
    print('Email de fluxo de agua enviado!')


#Cria o arquivo .csv para salvar as informações do banco de gasto de agua
def create_log_file_water():
    data_atual = datetime.now() # Obtém a data atual
    data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
    name_user = get_username()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\ConsumoAgua\\{data_string}_ConsumoAgua.csv"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\ConsumoAgua")
    path.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as arquivo:
        pass
    return log_file


# Faixa 1: Até 10.33 metros cúbicos (m³)
# Faixa 2: De 11 a 20 m³
# Faixa 3: Acima de 20 m³
# A tarifa para cada faixa é a seguinte:

# Faixa 1: R$ 2,50 por m³
# Faixa 2: R$ 3,00 por m³
# Faixa 3: R$ 4,00 por m³

# Função que calcula o gasto de agua de acordo com a tarifa sabesp
def calculate_fare(consumo):
    consumoM3 = consumo / 1000
    if consumoM3 <= 10.33:
        return round(consumoM3 * 2.5, 2)
    elif consumoM3 <= 20:
        return round((10 * 2.5) + ((consumoM3 - 10) * 3), 2)
    else:
        return round((10 * 2.5) + (10 * 3) + ((consumoM3 - 20) * 4), 2)

#Pega as informações do banco de consumo de agua, calcular o gasto de agua e enviar por e-mail
def calculate_send():
        
        cursor.execute(get_query_water)
        result = cursor.fetchall()
        consumption = create_log_file_water()
        consumption_money = 0.0

        with open(consumption, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Data', 'Gasto'])  # Escreve o cabeçalho

            for row in result:
                Data, Gasto  = row
                consumption_money = consumption_money + Gasto
                csvwriter.writerow([Data, Gasto])

        consumption_total = calculate_fare(consumption_money)

        send_email_water(consumption, consumption_total)
        print("Dados de gasto de aguá salvos no arquivo CSV")
        
#Função que realiza o agendamento das tarefas do servidor
def interface():

    #Agendar o envio do calculo da matriz de markov ao banco a cada 9 horas
    schedule.every(9).hours.do(markov.inserir_markov)

    #Agendar o envio de consumo de agua a cada 10 horas
    schedule.every(10).hours.do(calculate_send)

    # Agendar a coleta de dados da API a cada 3 minutos e envia ao banco de dados
    schedule.every(3).minutes.do(collect_data)

    # Agendar a função backup() a cada 10 horas
    schedule.every(10).hours.do(backup)


    while True:
        schedule.run_pending()
        time.sleep(1)


    # Fechar a conexão com o banco de dados ao final
    conn.close()
