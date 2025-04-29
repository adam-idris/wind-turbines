import argparse
from pipeline.io import load_group_csvs, save_dataframe, save_to_sqlite
from pipeline.cleaning import detect_and_treat_outliers, handle_missing_values
from pipeline.stats import compute_daily_stats
from pipeline.anomaly import flag_all_anomalies

def run_pipeline(input_dir: str, output_dir: str):
    raw     = load_group_csvs(input_dir)
    cleaned = detect_and_treat_outliers(raw)
    cleaned = handle_missing_values(cleaned)
    daily   = compute_daily_stats(cleaned)
    flagged = flag_all_anomalies(daily)

    # CSV outputs
    save_dataframe(cleaned, f"{output_dir}/cleaned_data.csv")
    save_dataframe(flagged, f"{output_dir}/daily_stats_with_anomalies.csv")

    # SQLite persistence
    save_to_sqlite(cleaned, 'cleaned_data')
    save_to_sqlite(flagged, 'daily_stats')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir',  default='data',   help='Folder containing raw CSVs')
    parser.add_argument('--output-dir', default='output', help='Folder to save outputs')
    args = parser.parse_args()
    run_pipeline(args.input_dir, args.output_dir)