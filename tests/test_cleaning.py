import pandas as pd
from pipeline.cleaning import handle_missing_values

def test_handle_missing_values():
    df = pd.DataFrame({
        'timestamp': ['2025-01-01 00:00', '2025-01-01 01:00'],
        'turbine_id': [1, 1],
        'wind_speed': [5.0, None],
        'wind_direction': [100, None],
        'power_output': [1.2, None]
    })
    out = handle_missing_values(df)
    assert not out['Power Output'].isna().any()
