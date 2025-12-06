import numpy as np
import pandas as pd

def wsm_ranking(X, pesos, tipos, criterios_final):
    """
    Ejecuta el método Weighted Sum Model (WSM)
    y retorna el ranking final.
    """

    # 1. Filtrar solo los criterios activos
    X_sel = X[criterios_final]

    # Filtrar pesos y normalizarlos
    idx = [list(X.columns).index(c) for c in criterios_final]
    pesos_sel = pesos[idx]
    pesos_sel = pesos_sel / pesos_sel.sum()

    # Filtrar tipos
    tipos_sel = {c: tipos[c] for c in criterios_final}

    # 2. Normalización
    X_norm = X_sel.copy()
    for c in criterios_final:
        col = X_sel[c]
        if tipos_sel[c] == "beneficio":
            X_norm[c] = (col - col.min()) / (col.max() - col.min())
        else:
            X_norm[c] = (col.max() - col) / (col.max() - col.min())

    # 3. Cálculo de puntajes WSM
    puntajes = X_norm.values @ pesos_sel

    ranking = pd.DataFrame({
        "Puntaje": puntajes
    }, index=X_sel.index).sort_values("Puntaje", ascending=False)

    return ranking, X_norm, pesos_sel
