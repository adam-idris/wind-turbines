import pandas as pd
import numpy as np
import pytest
from pipeline.cleaning import detect_and_treat_outliers, handle_missing_values

def test_detect_and_treat_outliers_basic():
    df = pd.DataFrame({
        'turbine_id': [1, 1, 1, 2, 2],
        'power_output': [10, 10, 1000, 5, 5]  # 1000 is an outlier for turbine 1
    })
    # with only three points [10,10,1000], z ≈ 1.41, so using z_thresh=1.0 will flag 1000
    out = detect_and_treat_outliers(df, z_thresh=1.0)
    # the extreme 1000 should become NaN
    assert np.isnan(out.loc[2, 'power_output'])
    # other values unchanged
    assert out.loc[0, 'power_output'] == 10

def test_handle_missing_values_interpolation():
    # two timestamps one hour apart, hole in both numeric cols
    df = pd.DataFrame({
        'timestamp': ['2025-01-01 00:00', '2025-01-01 01:00', '2025-01-01 02:00'],
        'turbine_id': [1, 1, 1],
        'wind_speed': [5.0, np.nan, 7.0],
        'wind_direction': [100, np.nan, 120],
        'power_output': [1.0, np.nan, 3.0]
    })
    out = handle_missing_values(df)
    # should interpolate the middle row to 6.0, 110, 2.0
    mid = out.iloc[1]
    assert pytest.approx(mid['wind_speed'], rel=1e-3) == 6.0
    assert pytest.approx(mid['wind_direction'], rel=1e-3) == 110.0
    assert pytest.approx(mid['power_output'], rel=1e-3) == 2.0

def test_handle_missing_values_drop_remaining():
    # if endpoints are NaN, interpolation leaves NaN—these should be dropped
    df = pd.DataFrame({
        'timestamp': ['2025-01-01 00:00', '2025-01-01 01:00'],
        'turbine_id': [1, 1],
        'wind_speed': [np.nan, 5.0],
        'wind_direction': [np.nan, 110],
        'power_output': [np.nan, 2.0]
    })
    out = handle_missing_values(df)
    # only the second row remains
    assert out.shape[0] == 1
    assert not out.isna().any().any()