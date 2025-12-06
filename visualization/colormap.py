import branca.colormap as cm
import numpy as np

def create_colormap(scores):
    min_val = np.min(scores)
    max_val = np.max(scores)

    if min_val == max_val:
        max_val = min_val + 1e-9

    return cm.linear.RdYlGn_09.scale(min_val, max_val)
