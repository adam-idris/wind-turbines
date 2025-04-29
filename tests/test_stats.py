import pandas as pd
from pipeline.stats import compute_daily_stats

def test_compute_daily_stats():
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(['2025-01-01', '2025-01-01']),
        'turbine_id': [1, 1],
        'power_output': [1.0, 3.0]
    })
    res = compute_daily_stats(df)
    assert res.iloc[0]['mean_output'] == 2.0
