# ============================================================
# FUNCTIONS
# ============================================================

import numpy as np
import pandas as pd


def calculate_hourly_profile(data):
    """
    Calculate mean NO2 concentration by hour and station type.
    """

    return (
        data
        .groupby(
            ["station_type", "hour"]
        )["no2"]
        .mean()
        .reset_index()
    )


def calculate_daily_mean(data):
    """
    Calculate daily mean NO2 concentration.
    """

    return (
        data
        .groupby(
            ["station", "date"]
        )["no2"]
        .mean()
        .reset_index()
    )


def calculate_r_squared(observed, predicted):
    """
    Calculate R-squared between observed and predicted values.
    """

    observed = np.asarray(observed)
    predicted = np.asarray(predicted)

    correlation = np.corrcoef(
        observed,
        predicted
    )[0, 1]

    return correlation ** 2
