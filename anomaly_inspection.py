"""
Script for visual inspection of turbine anomalies using multilayer detection.

This script reads the daily statistics (with anomaly flags) from the SQLite database,
plots time series of mean power output per turbine, and highlights anomaly days for:
- Statistical ±2σ (`stat_anomaly`)
- Power-curve residuals (`pc_anomaly`)
- IsolationForest (`iforest_anomaly`)
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
db_path = 'wind_turbines.db'
output_dir = 'output/plots'
os.makedirs(output_dir, exist_ok=True)

# Load data from SQLite
def load_daily_stats(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT * FROM daily_stats', conn, parse_dates=['date'])
    conn.close()
    # Ensure correct dtypes
    df['date'] = pd.to_datetime(df['date'])
    # Convert anomaly flags to boolean
    for col in ['stat_anomaly', 'pc_anomaly', 'iforest_anomaly']:
        if col in df.columns:
            df[col] = df[col].astype(bool)
        else:
            df[col] = False
    return df

def plot_turbine(df, tid, output_dir):
    sub = df[df['turbine_id'] == tid].sort_values('date')
    fig, ax = plt.subplots(figsize=(10, 5))
    # Plot mean output
    ax.plot(sub['date'], sub['mean_output'], label='Mean Output')
    # Highlight each anomaly type with different markers/colors
    if 'stat_anomaly' in sub.columns:
        sa = sub[sub['stat_anomaly']]
        ax.scatter(sa['date'], sa['mean_output'], marker='o', facecolors='none', edgecolors='orange', label='±2σ Anomaly', zorder=5)
    if 'pc_anomaly' in sub.columns:
        pa = sub[sub['pc_anomaly']]
        ax.scatter(pa['date'], pa['mean_output'], marker='x', color='red', label='Power-Curve Anomaly', zorder=5)
    if 'iforest_anomaly' in sub.columns:
        ia = sub[sub['iforest_anomaly']]
        ax.scatter(ia['date'], ia['mean_output'], marker='D', facecolors='none', edgecolors='purple', label='IsolationForest Anomaly', zorder=5)

    ax.set_title(f'Turbine {tid} Mean Output & Anomalies')
    ax.set_xlabel('Date')
    ax.set_ylabel('Mean Power Output (MW)')
    ax.legend()
    ax.grid(True)

    fig_path = os.path.join(output_dir, f'turbine_{tid}_anomalies.png')
    fig.savefig(fig_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved plot: {fig_path}")

if __name__ == '__main__':
    daily = load_daily_stats(db_path)
    turbines = daily['turbine_id'].unique()
    for tid in turbines:
        plot_turbine(daily, tid, output_dir)
    print(f"All plots saved to {output_dir}")
