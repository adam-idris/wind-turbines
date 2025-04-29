import os
import glob
import pandas as pd
import sqlite3

def load_group_csvs(input_dir: str = 'data') -> pd.DataFrame:
    """
    Load all group CSVs from the specified folder (default: 'data').
    """
    pattern = os.path.join(input_dir, 'data_group_*.csv')
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No CSVs found: {pattern}")
    dfs = [pd.read_csv(fp, parse_dates=['timestamp']) for fp in files]
    return pd.concat(dfs, ignore_index=True)

def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Save DataFrame to CSV at output_path, creating dirs as needed.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

def save_to_sqlite(df: pd.DataFrame,
                   table_name: str,
                   db_path: str = 'wind_turbines.db') -> None:
    """
    Persist DataFrame to SQLite table (replacing any existing table).
    """
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()