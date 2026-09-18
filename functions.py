import numpy as np
import pandas as pd

from scipy.spatial import cKDTree


def find_datetime_column(dataframe):
    """
    Identify the datetime column in the NO2 dataset.
    """

    preferred_names = [
        "Messzeit",
        "Datum",
        "date",
        "datetime",
        "timestamp"
    ]

    for column in preferred_names:

        if column in dataframe.columns:
            return column

    return dataframe.columns[0]


def clean_numeric(series):
    """
    Convert measurement values to numeric values.
    """

    values = (
        series
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    return pd.to_numeric(
        values,
        errors="coerce"
    )


def calculate_station_means(dataframe):
    """
    Calculate mean NO2 concentration per station.
    """

    return (
        dataframe
        .groupby("station")["no2"]
        .mean()
        .reset_index()
    )


def calculate_hourly_profile(dataframe):
    """
    Calculate average NO2 concentration by station type
    and hour of day.
    """

    return (
        dataframe
        .groupby(
            [
                "station_type",
                "hour"
            ]
        )["no2"]
        .mean()
        .reset_index()
    )


def idw(
    points,
    values,
    grid_x,
    grid_y,
    power=2
):
    """
    Perform inverse distance weighting.
    """

    tree = cKDTree(points)

    grid_points = np.column_stack(
        [
            grid_x.ravel(),
            grid_y.ravel()
        ]
    )

    distances, indices = tree.query(
        grid_points,
        k=len(points)
    )

    distances = np.maximum(
        distances,
        1e-12
    )

    weights = 1 / distances**power

    result = (
        np.sum(
            weights * values[indices],
            axis=1
        )
        /
        np.sum(
            weights,
            axis=1
        )
    )

    return result.reshape(
        grid_x.shape
    )


def regression_statistics(
    dataframe,
    x_column,
    y_column
):
    """
    Calculate linear regression statistics.
    """

    from scipy.stats import linregress

    clean = dataframe[
        [
            x_column,
            y_column
        ]
    ].dropna()

    result = linregress(
        clean[x_column],
        clean[y_column]
    )

    return {
        "n": len(clean),
        "slope": result.slope,
        "intercept": result.intercept,
        "r_squared": result.rvalue ** 2,
        "p_value": result.pvalue
    }
