import numpy as np
import pandas as pd

# 1. DEFINICIÓN DE CRITERIOS Y TIPOS

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

# 2. MATRIZ DE COMPARACIÓN AHP

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

# 3. FUNCIÓN: OBTENER PESOS Y CONSISTENCIA

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

# 4. MATRIZ DE ALTERNATIVAS

alternativas = [
    "ZONA_1","ZONA_2","ZONA_3","ZONA_4","ZONA_5",
    "ZONA_6","ZONA_7","ZONA_8","ZONA_9","ZONA_10"
]

X = pd.DataFrame({
    "C1_Áreas_protegidas":      [0.5, 8.0, 25.0, 2.2, 0.0, 40.0, 5.5, 12.0, 0.8, 18.0],
    "C2_Áreas_culturales":      [0, 1, 2, 0, 0, 3, 1, 4, 0, 2],
    "C3_Factor_riesgo":         [12, 28, 55, 20, 10, 72, 18, 38, 9, 45],
    "C4_Tasa_desempleo":        [18.0, 24.5, 15.2, 30.0, 12.5, 22.0, 9.0, 27.0, 8.5, 20.0],
    "C5_Inversión_pública":     [1200, 600, 3500, 200, 12000, 50, 800, 400, 25000, 1500],
    "C6_Percepción_seguridad":  [78, 62, 85, 40, 90, 30, 65, 55, 92, 70],
    "C7_Velocidad_viento":      [8.4, 6.1, 10.2, 5.0, 11.5, 4.6, 7.8, 6.5, 12.3, 9.0],
    "C8_Elevación_terreno":     [350,1200,800,150,600,50,2200,1400,900,1100],
    "C9_Pendiente_terreno":     [5.0,12.0,7.5,3.0,4.0,18.0,9.0,11.5,2.0,6.0],
    "C10_Distancia_turística":  [22.0,4.5,35.0,2.0,28.0,1.0,15.0,6.0,40.0,10.0],
    "C11_Índice_accesibilidad": [72,58,80,45,88,30,64,52,90,68],
    "C12_Grado_urbanización":   [12,45,8,60,5,75,20,35,3,30]
}, index=alternativas)

# 5. SELECCIÓN DE CRITERIOS (empty=all)

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

# 6. NORMALIZACIÓN SOLO DE LOS CRITERIOS SELECCIONADOS

X_norm = X_sel.copy()

for c in criterios_final:
    col = X_sel[c]
    if tipos_sel[c] == "beneficio":
        X_norm[c] = (col - col.min()) / (col.max() - col.min())
    else:
        X_norm[c] = (col.max() - col) / (col.max() - col.min())


# 7. PUNTUACIÓN FINAL (WSM)


puntajes = X_norm.values @ pesos_sel

ranking = pd.DataFrame({
    "Puntaje": puntajes
}, index=alternativas).sort_values("Puntaje", ascending=False)


# 8. SALIDAS WSM


print("\n=== CRITERIOS ACTIVOS ===")
print(criterios_final)

print("\n=== PESOS PARA LOS CRITERIOS ACTIVOS ===")
for c, p in zip(criterios_final, pesos_sel):
    print(f"{c:30}  {p:.4f}")

print("\nCR Consistencia:", CR)

print("\n=== RANKING FINAL WSM ===")
print(ranking)