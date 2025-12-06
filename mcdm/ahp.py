import numpy as np
import pandas as pd

def compute_weights(pairwise_matrix):
    eigvals, eigvecs = np.linalg.eig(pairwise_matrix)
    max_index = np.argmax(eigvals)
    max_eigvec = np.real(eigvecs[:, max_index])
    weights = max_eigvec / max_eigvec.sum()
    return weights

def consistency_ratio(pairwise_matrix):
    n = pairwise_matrix.shape[0]
    eigvals = np.linalg.eigvals(pairwise_matrix)
    lambda_max = np.max(np.real(eigvals))

    CI = (lambda_max - n) / (n - 1)

    # Tabla de RI
    RI_table = {
        1: 0.00,
        2: 0.00,
        3: 0.52,
        4: 0.89,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45,
        10: 1.49,
        11: 1.51,
        12: 1.48,
        13: 1.56,
        14: 1.57,
        15: 1.59
    }

    if n not in RI_table:
        raise ValueError(f"No RI value available for n={n}. Please extend RI_table.")

    RI = RI_table[n]
    CR = CI / RI
    return CR
