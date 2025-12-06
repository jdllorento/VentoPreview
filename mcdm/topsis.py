import numpy as np
import pandas as pd

def topsis(matrix, weights, criteria_types):
    matrix = matrix.astype(float)

    # 1. Normalización
    col_sums = np.sqrt((matrix ** 2).sum(axis=0))

    col_sums[col_sums == 0] = 1e-12

    R = matrix / col_sums

    # 2. Matriz ponderada
    V = R * weights

    # 3. Ideales
    ideal_pos = []
    ideal_neg = []

    for col, crit in enumerate(criteria_types):
        if crit == 'benefit':
            ideal_pos.append(V.iloc[:, col].max())
            ideal_neg.append(V.iloc[:, col].min())
        else:
            ideal_pos.append(V.iloc[:, col].min())
            ideal_neg.append(V.iloc[:, col].max())

    # 4. Distancias a los ideales
    ideal_pos = pd.Series(ideal_pos, index=V.columns)
    ideal_neg = pd.Series(ideal_neg, index=V.columns)

    S_pos = np.sqrt(((V - ideal_pos)**2).sum(axis=1))
    S_neg = np.sqrt(((V - ideal_neg)**2).sum(axis=1))

    # 5. Scores
    C = S_neg / (S_pos + S_neg)

    return C, V, ideal_pos, ideal_neg
