import mysql.connector

# Conectar ao banco de dados MySQL (db4free.net)
conn = mysql.connector.connect(
    host='', # Substitua pelo endereço IP ou nome do host do seu servidor MySQL
    user='',   # Substitua pelo nome de usuário do MySQL
    password='', # Substitua pela senha do MySQL
    database=''  # Substitua pelo nome do banco de dados
)
cursor = conn.cursor()

# Consulta SELECT para recuperar informações da tabela
select_query = '''
    SELECT data, temperatura, umidade, descricao
    FROM previsao
    LIMIT 10
'''

cursor.execute(select_query)
result = cursor.fetchall()

for row in result:
    data, temperatura, umidade, descricao = row
    print(f"Data: {data}, Temperatura: {temperatura}, Umidade: {umidade}, Descrição: {descricao}")

# Fechar a conexão com o banco de dados
conn.close()
