import mysql.connector
import datetime
import locale
import numpy as np

# Configurar opções de exibição para arredondar números e não usar notação científica
np.set_printoptions(precision=2, suppress=True)

# Definir a localização para pt-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

# Obter o mês atual
mes_atual = datetime.datetime.now().strftime('%B').capitalize().upper()

# Obtenha a data atual
data_atual = datetime.datetime.now()

# Extraia o ano da data atual
ano_atual = data_atual.year

MATRIZES_MARKOV = {
    #Matriz de markov referente ao mês de Janeiro definindo a probabilidades mês em 2023
    'JANEIRO' : np.array([
        [1, 0],
        [0, 1]
    ]),

    #Matriz de markov referente ao mês de Fevereiro definindo a probabilidades mês em 2023
    'FEVEREIRO' : np.array([
        [0.83, 1],
        [0.17, 0]
    ]),

    #Matriz de markov referente ao mês de Março definindo a probabilidades mês em 2023
    'MARCO' : np.array([
        [0, 1],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Abril definindo a probabilidades mês em 2023
    'ABRIL' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Maio definindo a probabilidades mês em 2023
    'MAIO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Junho definindo a probabilidades mês em 2023
    'JUNHO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Julho definindo a probabilidades mês em 2023
    'JUNLHO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Agosto definindo a probabilidades mês em 2023
    'AGOSTO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Setembro definindo a probabilidades mês em 2023
    'SETEMBRO' : np.array([
        [0.83, 1],
        [0.17, 0]
    ]),

    #Matriz de markov referente ao mês de Outubro definindo a probabilidades mês em 2023
    'OUTUBRO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Novembro definindo a probabilidades mês em 2023
    'NOVEMBRO' : np.array([
        [0, 0],
        [0, 0]
    ]),

    #Matriz de markov referente ao mês de Dezembro definindo a probabilidades mês em 2023
    'DEZEMBRO' : np.array([
        [0, 0],
        [0, 0]
    ]),

}

ANO_REFERENCIA = {

    '2023' : 1,
    '2024' : 2,
    '2025' : 3,
    '2026' : 4,
    '2027' : 5

}

def inserir_markov():

    # Conectar ao banco de dados MySQL (db4free.net)
    conn = mysql.connector.connect(
        host='85.10.205.173', # Substitua pelo endereço IP ou nome do host do seu servidor MySQL
        user='',   # Substitua pelo nome de usuário do MySQL
        password='', # Substitua pela senha do MySQL
        database='tccarduino2023'  # Substitua pelo nome do banco de dados
    )

    cursor = conn.cursor()

    # Criar a tabela se ela não existir
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Markov{ano_atual} (
            Mes TEXT,      
            Probabilidade FLOAT
        )
    ''')
    conn.commit()

    # Inserir informações no banco de dados
    insert_query = f'''
        INSERT INTO Markov{ano_atual} (Mes, Probabilidade)
        VALUES (%s, %s)
    '''

    # Coleta a matriz de acordo com o mês atual
    matriz_atual = MATRIZES_MARKOV.get(mes_atual)

    # Coleta a key de referencia de acordo com o ano atual
    referencia = ANO_REFERENCIA.get(f'{ano_atual}')

    #Realiza o calculo da matriz de markov de acordo com o ano e mês atual
    calculo = np.linalg.matrix_power(matriz_atual, referencia)

    #Coleta a probabilidade do mês atual ser um mês chuvoso
    PROBABILIDADE_CHUVA = float(calculo[0][0])

    values = (mes_atual, PROBABILIDADE_CHUVA)
    cursor.execute(insert_query, values)
    conn.commit()
    print(f"Dados do calculo de Markov referente ao mês de {mes_atual} do ano de {ano_atual} inseridos no banco de dados")

inserir_markov()

