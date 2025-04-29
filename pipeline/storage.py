import sqlite3
import pandas as pd

def save_to_sqlite(df: pd.DataFrame, table_name: str, db_path: str = 'wind_turbines.db'):
    conn = sqlite3.connect(db_path)
    # Write dataframe, replacing existing table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()