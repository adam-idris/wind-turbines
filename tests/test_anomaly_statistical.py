import pandas as pd
from pipeline.anomaly import flag_statistical_anomalies as flag_stat

def test_flag_statistical_anomalies_no_flags():
    # strictly increasing mean_output, early 30-day baseline → no flags
    dates = pd.date_range('2025-01-01', periods=31).date
    df = pd.DataFrame({
        'date': dates,
        'turbine_id': [1]*31,
        'mean_output': list(range(31)),
        'mean_wind_speed': [5]*31,
        'mean_wind_direction': [0]*31
    })
    out = flag_stat(df)
    assert out['stat_anomaly'].sum() == 0

def test_flag_statistical_anomalies_with_flag():
    # create a large jump on day 31
    dates = pd.date_range('2025-01-01', periods=31).date
    means = list(range(31))
    means[-1] = means[-2] + 100  # extreme
    df = pd.DataFrame({
        'date': dates,
        'turbine_id': [1]*31,
        'mean_output': means,
        'mean_wind_speed': [5]*31,
        'mean_wind_direction': [0]*31
    })
    out = flag_stat(df)
    assert out.loc[out['date']==dates[-1], 'stat_anomaly'].iloc[0]
