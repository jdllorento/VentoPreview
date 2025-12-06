import pandas as pd

from mcdm.ahp import compute_weights, consistency_ratio
from mcdm.topsis import topsis
from visualization.folium_map import create_topsis_map

# 1. Cargar alternativas
alts = pd.read_csv("data/alternatives.csv")

# Extraemos los criterios
matrix = alts.drop(columns=["id","nombre", "lat", "lon"])


# 2. Cargar criterios y sus tipos
df_criterios = pd.read_csv("data/criteria.csv")

criterios = df_criterios["criterio"].tolist()
tipos = df_criterios["tipo"].tolist()

assert all(c in matrix.columns for c in criterios), "ERROR: Faltan criterios en alternatives.csv"

matrix = matrix[criterios]


# 3. Cargar matriz de comparación por pares (AHP)
pairwise = pd.read_csv("data/pairwise_matrix.csv", header=None).values

weights = compute_weights(pairwise)
CR = consistency_ratio(pairwise)

print("Índice de Consistencia (CR):", CR)
print("Pesos AHP:", weights)


# 4. Ejecutar TOPSIS
scores, V, ideal_pos, ideal_neg = topsis(matrix, weights, tipos)

# Agregar puntajes al dataframe de alternativas
alts["score"] = scores

print(alts["score"])
print("Min:", alts["score"].min())
print("Max:", alts["score"].max())

# 5. Crear mapa con Folium
m = create_topsis_map(alts)
m.save("map_output.html")

print("Mapa generado: map_output.html")
