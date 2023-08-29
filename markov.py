
import pandas as pd
import datetime
import locale
import numpy as np

# Definir a localização para pt-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

# Obter o mês atual
mes_atual = datetime.datetime.now().strftime('%B').capitalize()

# Ler a planilha Excel usando o pandas
excel_file = 'Santo amaro indices.xlsx'
df = pd.read_excel(excel_file)

# Acessar o valor da célula da coluna 'Agosto' e linha 22
valor = df.at[0, f'{mes_atual}']  # 21 porque os índices de linha em Python começam em 0

# Criar matrizes
A = np.array([[valor, 2.0], [3.0, 4.0]])
B = np.array([[5.0], [8.0]])

# Multiplicação de matrizes
produto = np.dot(A, B)
produto2 = int(produto[0][0])
print(produto2)