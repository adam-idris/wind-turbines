import os
import sqlite3
import pandas as pd
import pytest
from pipeline.io import load_group_csvs, save_dataframe, save_to_sqlite

def make_csv(tmp_path, idx):
    df = pd.DataFrame({
        'timestamp': ['2025-01-01 00:00', '2025-01-01 01:00'],
        'turbine_id': [idx, idx],
        'wind_speed': [5.0, 6.0],
        'wind_direction': [100, 110],
        'power_output': [1.2, 1.4]
    })
    path = tmp_path / f"data_group_{idx}.csv"
    df.to_csv(path, index=False)
    return path

def test_load_group_csvs(tmp_path):
    # create two group files
    files = [make_csv(tmp_path, i) for i in (1,2)]
    combined = load_group_csvs(str(tmp_path))
    # expect 4 rows, 5 columns
    assert combined.shape == (4, 5)
    assert set(combined.columns) == {'timestamp','turbine_id','wind_speed','wind_direction','power_output'}

def test_load_group_no_files(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_group_csvs(str(tmp_path))

def test_save_dataframe(tmp_path):
    df = pd.DataFrame({'a':[1,2,3]})
    out = tmp_path / "sub/dir/out.csv"
    save_dataframe(df, str(out))
    df2 = pd.read_csv(out)
    assert df2['a'].tolist() == [1,2,3]

def test_save_to_sqlite(tmp_path):
    df = pd.DataFrame({'a':[1,2,3]})
    db = tmp_path / "test.db"
    save_to_sqlite(df, 'tbl', db_path=str(db))
    # verify via sqlite3
    conn = sqlite3.connect(str(db))
    df2 = pd.read_sql("SELECT * FROM tbl ORDER BY a", conn)
    conn.close()
    assert df2['a'].tolist() == [1,2,3]
