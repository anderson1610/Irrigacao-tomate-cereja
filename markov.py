import pandas as pd
import datetime
import locale
import numpy as np

# Configurar opções de exibição para arredondar números e não usar notação científica
np.set_printoptions(precision=2, suppress=True)

# Definir a localização para pt-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

# Obter o mês atual
mes_atual = datetime.datetime.now().strftime('%B').capitalize()

# Ler a planilha Excel usando o pandas
excel_file = 'Santo amaro indices.xlsx'
df = pd.read_excel(excel_file)

# Acessar o valor da célula da coluna 'Agosto' e linha 
valor = df.at[0, f'{mes_atual}']  # 21 porque os índices de linha em Python começam em 0

# definindo a matriz de probabilidades mês x em 2023
M1 = np.array([
    [valor, 0],
    [0, 0]
])

# calculando a matriz probabilidades mês x em 2024
M2 = np.linalg.matrix_power(M1, 2)

# Multiplicação de matrizes
produto = np.dot(M1, M2)
produto2 = int(produto[0][0])
print(M1)
