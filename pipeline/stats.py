import pandas as pd

def compute_daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes daily summary statistics for each turbine, including wind statistics.
    """
    dfc = df.copy()
    dfc['date'] = dfc['timestamp'].dt.date

    # Aggregate power and wind metrics per turbine per day
    agg = dfc.groupby(['date', 'turbine_id']).agg(
        min_output=('power_output', 'min'),
        max_output=('power_output', 'max'),
        mean_output=('power_output', 'mean'),
        mean_wind_speed=('wind_speed', 'mean'),
        mean_wind_direction=('wind_direction', 'mean')
    ).reset_index()

    return agg