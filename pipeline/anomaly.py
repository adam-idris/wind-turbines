import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

EARLY_DAYS = 30

def flag_statistical_anomalies(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags days where mean_output deviates ±2σ from the first EARLY_DAYS baseline.
    """
    df = daily_df.copy()
    df['stat_anomaly'] = False
    df['date'] = pd.to_datetime(df['date'])

    for tid, grp in df.groupby('turbine_id'):
        baseline = grp.sort_values('date').head(EARLY_DAYS)
        mu = baseline['mean_output'].mean()
        sigma = baseline['mean_output'].std()
        mask = grp['mean_output'].lt(mu - 2*sigma) | grp['mean_output'].gt(mu + 2*sigma)
        df.loc[mask.index, 'stat_anomaly'] = mask

    df['date'] = df['date'].dt.date
    return df

def flag_power_curve_anomalies(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fits a linear regression of mean_output on mean_wind_speed using baseline data,
    then flags residuals outside ±2σ.
    """
    df = daily_df.copy()
    df['pc_anomaly'] = False

    for tid, grp in df.groupby('turbine_id'):
        # Prepare features
        X = grp[['mean_wind_speed']].values
        y = grp['mean_output'].values

        # Fit on the baseline period
        model = LinearRegression().fit(X[:EARLY_DAYS], y[:EARLY_DAYS])
        preds = model.predict(X)
        residuals = y - preds

        mu = residuals[:EARLY_DAYS].mean()
        sigma = residuals[:EARLY_DAYS].std()
        mask = (residuals < mu - 2*sigma) | (residuals > mu + 2*sigma)
        df.loc[grp.index[mask], 'pc_anomaly'] = True

    return df

def flag_iforest_anomalies(daily_df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Applies IsolationForest on [mean_output, mean_wind_speed, mean_wind_direction].
    """
    df = daily_df.copy()
    iso = IsolationForest(contamination=contamination, random_state=42)
    features = df[['mean_output', 'mean_wind_speed', 'mean_wind_direction']].values
    labels = iso.fit_predict(features)
    df['iforest_anomaly'] = labels == -1
    return df

def flag_all_anomalies(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes all three anomaly detection layers in sequence.
    """
    df = flag_statistical_anomalies(daily_df)
    df = flag_power_curve_anomalies(df)
    df = flag_iforest_anomalies(df)
    return df