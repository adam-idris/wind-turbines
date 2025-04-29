"""
Data cleaning: missing value imputation and outlier handling
"""
import pandas as pd
import numpy as np
from scipy import stats


def detect_and_treat_outliers(df: pd.DataFrame, z_thresh: float = 3.0) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy['z_score'] = (
        df_copy.groupby('turbine_id')['power_output']
               .transform(lambda x: np.abs(stats.zscore(x, nan_policy='omit')))
    )
    df_copy.loc[df_copy['z_score'] > z_thresh, 'power_output'] = np.nan
    return df_copy.drop(columns='z_score')


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure timestamp is datetime and set as index
    dfc = df.copy()
    dfc['timestamp'] = pd.to_datetime(dfc['timestamp'])
    dfc = dfc.sort_values(['turbine_id', 'timestamp']).set_index('timestamp')
    # Columns to interpolate
    cols = ['wind_speed', 'wind_direction', 'power_output']
    # Perform time-based interpolation per turbine for each column
    for col in cols:
        dfc[col] = dfc.groupby('turbine_id')[col].transform(lambda s: s.interpolate(method='time'))
    # Reset index, drop rows still containing NaNs in critical columns
    dfc = dfc.reset_index()
    return dfc.dropna(subset=cols)