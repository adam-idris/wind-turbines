import pandas as pd
from pipeline.io import load_group_csvs

def test_load_group_csvs(tmp_path):
    for i in range(2):
        df = pd.DataFrame({
            'timestamp': ['2025-01-01'],
            'turbine_id': [i],
            'wind_speed': [5],
            'wind_direction': [100],
            'power_output': [1.0]
        })
        (tmp_path / f"data_group_{i}.csv").write_text(df.to_csv(index=False))
    out = load_group_csvs(str(tmp_path))
    assert out.shape[0] == 2
