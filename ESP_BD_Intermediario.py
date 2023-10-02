from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
