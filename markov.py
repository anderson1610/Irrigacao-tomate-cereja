# importando numpy
import numpy as np

# definindo a matriz
# probabilidades semana 1
M1 = np.array([
    [0.7, 0.1],
    [0.3, 0.9]
])

# calculando a matriz
# probabilidades semana 2
M2 = np.linalg.matrix_power(M1, 2)

# definindo grupo
# semana 1
grupo_semana1 = np.array([
    [0.4],
    [0.6]
])

# calculando grupo
# semana 3
grupo_semana3 = np.matmul(M2, grupo_semana1)
print(grupo_semana3)