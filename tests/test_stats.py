import pandas as pd
from pipeline.stats import compute_daily_stats

def test_compute_daily_stats_basic():
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(['2025-01-01','2025-01-01','2025-01-02']),
        'turbine_id': [1,1,1],
        'power_output': [1.0,3.0,5.0],
        'wind_speed': [4.0,6.0,8.0],
        'wind_direction': [100,120,140]
    })
    stats = compute_daily_stats(df)
    # Expect two dates × one turbine = 2 rows
    assert set(stats['date']) == {pd.to_datetime('2025-01-01').date(), pd.to_datetime('2025-01-02').date()}
    # Check aggregates
    row = stats[stats['date']==pd.to_datetime('2025-01-01').date()].iloc[0]
    assert row['min_output']==1.0 and row['max_output']==3.0 and row['mean_output']==2.0
    assert row['mean_wind_speed']==5.0 and row['mean_wind_direction']==110.0
