import numpy as np
import pandas as pd

from scipy.spatial import cKDTree


def clean_numeric(series):
    series = (
        series.astype(str)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    return pd.to_numeric(series, errors="coerce")


def idw(points, values, grid_x, grid_y, power=2):
    tree = cKDTree(points)

    grid = np.column_stack(
        [grid_x.ravel(), grid_y.ravel()]
    )

    distances, indexes = tree.query(
        grid,
        k=len(points)
    )

    distances = np.maximum(distances, 1e-12)

    weights = 1 / distances**power

    result = (
        np.sum(weights * values[indexes], axis=1)
        / np.sum(weights, axis=1)
    )

    return result.reshape(grid_x.shape)


def r_squared(y, y_pred):
    y = np.asarray(y)
    y_pred = np.asarray(y_pred)

    return 1 - (
        np.sum((y - y_pred) ** 2)
        / np.sum((y - y.mean()) ** 2)
    )
