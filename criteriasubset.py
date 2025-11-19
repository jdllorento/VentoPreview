import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 1. DEFINICIÓN DE CRITERIOS Y TIPOS
# ------------------------------------------------------------

criterios = [
    "C1_Áreas_protegidas",
    "C2_Áreas_culturales",
    "C3_Factor_riesgo",
    "C4_Tasa_desempleo",
    "C5_Inversión_pública",
    "C6_Percepción_seguridad",
    "C7_Velocidad_viento",
    "C8_Elevación_terreno",
    "C9_Pendiente_terreno",
    "C10_Distancia_turística",
    "C11_Índice_accesibilidad",
    "C12_Grado_urbanización"
]

# Criterios costo / beneficio
tipos = {
    "C1_Áreas_protegidas": "costo",
    "C2_Áreas_culturales": "costo",
    "C3_Factor_riesgo": "costo",
    "C4_Tasa_desempleo": "beneficio",
    "C5_Inversión_pública": "beneficio",
    "C6_Percepción_seguridad": "beneficio",
    "C7_Velocidad_viento": "beneficio",
    "C8_Elevación_terreno": "beneficio",
    "C9_Pendiente_terreno": "costo",
    "C10_Distancia_turística": "beneficio",
    "C11_Índice_accesibilidad": "beneficio",
    "C12_Grado_urbanización": "beneficio"
}

# ------------------------------------------------------------
# 2. MATRIZ DE COMPARACIÓN AHP
# ------------------------------------------------------------

A = np.array([
    [1,   2,   2,   5,   4,   5,   1/5, 3,   3,   2,   3,   3],
    [1/2, 1,   1,   4,   3,   4,   1/6, 2,   2,   2,   2,   2],
    [1/2, 1,   1,   4,   3,   3,   1/7, 2,   2,   2,   2,   2],
    [1/5, 1/4, 1/4, 1,   1/2, 1/2, 1/9, 1/2, 1/2,1/3,1/3,1/3],
    [1/4, 1/3, 1/3, 2,   1,   2,   1/6, 2,   2,   2,   2,   2],
    [1/5, 1/4, 1/3, 2,   1/2, 1,   1/9, 1,   1,   1,   1,   1],
    [5,   6,   7,   9,   6,   9,   1,   5,   5,   7,   7,   7],
    [1/3, 1/2, 1/2, 2,   1/2, 1,   1/5, 1,   1,   1,   1,   1],
    [1/3, 1/2, 1/2, 2,   1/2, 1,   1/5, 1,   1,   1,   1,   1],
    [1/2, 1/2, 1/2, 3,   1/2, 1,   1/7, 1,   1,   1,   1,   1],
    [1/3, 1/2, 1/2, 3,   1/2, 1,   1/7, 1,   1,   1,   1,   1],
    [1/3, 1/2, 1/2, 3,   1/2, 1,   1/7, 1,   1,   1,   1,   1]
], dtype=float)

# ------------------------------------------------------------
# 3. FUNCIÓN: OBTENER PESOS Y CONSISTENCIA
# ------------------------------------------------------------

def pesos_y_CR(A):
    vals, vecs = np.linalg.eig(A)
    idx = np.argmax(vals.real)
    w = vecs[:, idx].real
    w = w / w.sum()
    n = A.shape[0]
    lambda_max = vals[idx].real
    CI = (lambda_max - n) / (n - 1)
    RI = 1.48  # Para n=12
    CR = CI / RI
    return w, CR

pesos, CR = pesos_y_CR(A)

# ------------------------------------------------------------
# 4. MATRIZ DE ALTERNATIVAS
# ------------------------------------------------------------

alternativas = [
    "ZONA_1","ZONA_2","ZONA_3","ZONA_4","ZONA_5",
    "ZONA_6","ZONA_7","ZONA_8","ZONA_9","ZONA_10"
]

X = pd.DataFrame({
    "C1_Áreas_protegidas":      [10.2,  0.0,  4.5, 18.0,  2.2, 30.0,  1.0,  8.8,  0.3, 12.0],
    "C2_Áreas_culturales":      [ 3,    1,    0,    2,    4,   1,    3,    0,    2,    5],
    "C3_Factor_riesgo":         [40,   15,   70,   25,   10,  45,   60,   18,   12,  22],
    "C4_Tasa_desempleo":        [22.5, 30.0,  9.8, 15.0, 27.0, 12.0, 18.5,  8.0, 25.0, 21.0],
    "C5_Inversión_pública":     [2200, 8000, 120, 500, 3000, 200, 900, 25000, 180, 600],
    "C6_Percepción_seguridad":  [55,   72,   40,  90,   30,  65,   82,   45,   95,   60],
    "C7_Velocidad_viento":      [7.5,  5.8, 11.2, 4.0, 10.8, 6.0,  9.5,  5.2, 12.5, 8.0],
    "C8_Elevación_terreno":     [1200, 350, 2000, 500, 900, 150, 1600, 800, 2500, 1100],
    "C9_Pendiente_terreno":     [12.0,  3.0, 18.0,  4.5, 7.0,  2.5,  9.0,  6.0,  1.0,  8.0],
    "C10_Distancia_turística":  [ 3.0, 25.0, 10.0,  5.5, 40.0,  2.0,  6.5, 12.0, 35.0, 15.0],
    "C11_Índice_accesibilidad": [65,   80,   50,   90,   45,   70,   55,   88,   40,   78],
    "C12_Grado_urbanización":   [25,   10,   45,   5,    30,   60,   20,   75,   8,    55]
}, index=alternativas)


# ------------------------------------------------------------
# 5. SELECCIÓN DE CRITERIOS (empty=all)
# ------------------------------------------------------------

criterios_seleccionados = [

]

# Criterios no excluibles
obligatorios = [
    "C7_Velocidad_viento",
    "C8_Elevación_terreno",
    "C9_Pendiente_terreno"
]

if criterios_seleccionados:

    for c in obligatorios:
        if c not in criterios_seleccionados:
            exit(f"Error: El criterio obligatorio '{c}' no puede ser excluido.")
    
    criterios_final = criterios_seleccionados

else:
    criterios_final = criterios

# Filtrar pesos según criterios seleccionados
indices = [criterios.index(c) for c in criterios_final]
pesos_sel = pesos[indices]
pesos_sel = pesos_sel / pesos_sel.sum()  # renormalizar

# Filtrar dataframe y tipos
X_sel = X[criterios_final]
tipos_sel = {c: tipos[c] for c in criterios_final}

# ------------------------------------------------------------
# 6. NORMALIZACIÓN SOLO DE LOS CRITERIOS SELECCIONADOS
# ------------------------------------------------------------

X_norm = X_sel.copy()

for c in criterios_final:
    col = X_sel[c]
    if tipos_sel[c] == "beneficio":
        X_norm[c] = (col - col.min()) / (col.max() - col.min())
    else:
        X_norm[c] = (col.max() - col) / (col.max() - col.min())

# ------------------------------------------------------------
# 7. PUNTUACIÓN FINAL (WSM)
# ------------------------------------------------------------

puntajes = X_norm.values @ pesos_sel

ranking = pd.DataFrame({
    "Puntaje": puntajes
}, index=alternativas).sort_values("Puntaje", ascending=False)

# ------------------------------------------------------------
# 8. SALIDAS
# ------------------------------------------------------------

print("\n=== CRITERIOS ACTIVOS ===")
print(criterios_final)

print("\n=== PESOS PARA LOS CRITERIOS ACTIVOS ===")
for c, p in zip(criterios_final, pesos_sel):
    print(f"{c:30}  {p:.4f}")

print("\nCR Consistencia:", CR)

print("\n=== RANKING FINAL ===")
print(ranking)
