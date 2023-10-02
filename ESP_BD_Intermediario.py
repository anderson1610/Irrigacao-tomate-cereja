from flask import Flask, request, jsonify
import mysql.connector
import datetime

app = Flask(__name__)

# Obtenha a data atual
data_atual = datetime.datetime.now()

# Extraia o ano da data atual
ano_atual = data_atual.year

# Configurações de conexão com o banco de dados
db_config = {
    'user': 'anderson1610',
    'password': '',
    'host': '85.10.205.173', # Normalmente, o host é o endereço IP do servidor MySQL no db4free
    'database': 'tccarduino2023' # Nome do banco de dados
}

@app.route('/adicionar_dados', methods=['POST'])
def adicionar_dados():
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Recupere os dados enviados pelo ESP8266 como JSON
        data = request.get_json()

        # Execute uma consulta de inserção no banco de dados
        sql = "INSERT INTO CustoAgua (Data, Gasto) VALUES (%s, %s)"
        val = (data['Data'], data['Gasto'])
        cursor.execute(sql, val)

        # Confirme a transação e feche a conexão
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Dados inseridos com sucesso!"})

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/obter_dados_markov', methods=['GET'])
def obter_dados_markov():
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Executar uma consulta para obter a última linha da planilha Markov2023
        sql = f"SELECT Mes, Probabilidade FROM Markov{ano_atual} WHERE ID = (SELECT MAX(ID) FROM Markov{ano_atual})"
        cursor.execute(sql)

        # Recuperar o resultado
        result = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        connection.close()

        if result:
            data = {'Mes': result[0], 'Probabilidade': result[1]}
            return jsonify(data)
        else:
            return jsonify({"error": "Nenhum dado encontrado"})

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/obter_ultima_previsao', methods=['GET'])
def obter_ultima_previsao():
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Executar uma consulta para obter a linha com o maior valor na coluna `ID`
        sql = "SELECT temperatura, umidade FROM previsao WHERE ID = (SELECT MAX(ID) FROM previsao)"
        cursor.execute(sql)

        # Recuperar o resultado
        result = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        connection.close()

        if result:
            temperatura, umidade = result
            return jsonify({"temperatura": temperatura, "umidade": umidade})
        else:
            return jsonify({"error": "Nenhum dado encontrado na planilha 'previsao'"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
