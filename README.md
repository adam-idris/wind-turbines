# Wind Turbine Performance Monitoring Pipeline

## Introduction & Context

Renewable energy is critical to the global transition away from fossil fuels. Wind farms, composed of dozens or hundreds of turbines, generate electricity by converting wind into mechanical power and then into electricity. Ensuring each turbine operates efficiently and detecting malfunctions early can save millions in downtime and maintenance costs.

This project implements an end-to-end, industry-grade data pipeline for monitoring wind turbine performance. It:

1. **Ingests** high-frequency sensor data (wind speed, wind direction, power output) for multiple turbines from CSV files.  
2. **Cleans** the data, handling missing readings and outliers.  
3. **Aggregates** into daily statistics per turbine.  
4. **Detects anomalies** through layered techniques—from simple statistical thresholds to machine learning models.  
5. **Stores** results in both CSV files and a SQLite database for easy querying and integration with other systems.  
6. **Visualises** anomalies with professional plots.  

By combining domain knowledge (power curves) with statistical and machine learning methods, this pipeline delivers robust insights for operational teams.

---

## Architecture & Code Structure

```
wind_turbine_pipeline/
├── data/                       # Raw CSV inputs (data_group_*.csv)
├── output/                     # CSV outputs and generated plots
├── pipeline/                   # Core modules
│   ├── io.py                   # File I/O & SQLite persistence
│   ├── cleaning.py            # Missing data interpolation & outlier treatment
│   ├── stats.py               # Daily summary statistics aggregation
│   ├── anomaly.py             # Multilayer anomaly detection
│   └── main.py                # Entry-point CLI orchestrating the pipeline
├── anomaly_inspection.py      # Standalone script for plotting anomalies
├── tests/                      # pytest suite for unit testing
├── requirements.txt           # Project dependencies
├── visual_notebook.ipynb      # Some analyses of results using visualisations
└── wind_turbines.db           # SQLite database (auto-created)
```

### Workflow

1. **Load** raw CSVs automatically from `data/`.  
2. **Detect outliers**: replace extreme power readings (|Z-score|>3) with NaN.  
3. **Impute missing** values via time-based interpolation per turbine.  
4. **Compute** daily metrics: min, max, mean power; mean wind speed; mean wind direction.  
5. **Flag anomalies** using three layers:
   - **Statistical**: ±2σ on daily mean output baseline.  
   - **Power-curve**: linear regression residuals of power vs. wind speed.  
   - **Machine-learning**: IsolationForest on multivariate features.  
6. **Persist** cleaned data and flagged summaries to CSV and SQLite (`wind_turbines.db`).  
7. **Visualise** with `anomaly_inspection.py`, producing per-turbine plots that highlight each anomaly type and general analyses using `visual_notebook.ipynb`.

---

## Tools & Libraries

| Component                  | Library                | Purpose & Reasoning                                              |
|----------------------------|------------------------|------------------------------------------------------------------|
| Data Processing            | **pandas**, **NumPy**  | Efficient DataFrame operations and numerical computations.       |
| Statistical Functions      | **SciPy**              | Z-score calculation for outlier detection.                      |
| Machine Learning           | **scikit-learn**       | IsolationForest and LinearRegression for advanced anomaly detection. |
| Database Persistence       | **sqlite3**            | Lightweight, file-based DB for easy integration and querying.     |
| Plotting                   | **matplotlib**         | High-quality, customizable visualizations of anomalies.           |
| Testing                    | **pytest**             | Rapid, expressive unit tests ensuring code reliability.          |
| CLI & Packaging            | **argparse**, **virtualenv** | Standard Python tooling for CLI interfaces and environment management. |

**Why these choices?**  
- **pandas & NumPy** are industry standards for tabular and numerical data, offering speed and convenience.  
- **SciPy Z-score** is a simple, interpretable method for catching gross sensor errors.  
- **scikit-learn** allows flexible modeling—IsolationForest captures complex, nonlinear patterns, while linear regression establishes interpretable power curves.  
- **SQLite** requires no separate server and integrates seamlessly via Python’s standard library.  
- **matplotlib** provides full control over styling for professional plots.  
- **pytest** yields clear, maintainable tests and fixtures.

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/adam-idris/wind-turbines.git
cd wind_turbine_pipeline

# (Optional) create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode (pulls install_requires from setup.py)
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

*requirements.txt*:
```
pandas
numpy
scipy
scikit-learn
matplotlib
pytest
```

---

## Usage

### Run the Full Pipeline
```bash
# Default: reads from ./data, writes to ./output and wind_turbines.db
python -m pipeline.main
```
Override paths:
```bash
python -m pipeline.main --input-dir path/to/data --output-dir path/to/output
```

### Visualize Anomalies
```bash
python anomaly_inspection.py
```
Plots saved to `output/plots/`.

---

## Configuration

- **Z-score threshold**: adjust `z_thresh` in `detect_and_treat_outliers`.  
- **Baseline window**: modify `EARLY_DAYS` in `anomaly.py`.  
- **IsolationForest parameters**: pass `contamination` to `flag_iforest_anomalies`.

---

## Testing

```bash
pytest
```
Coverage focuses on edge cases: empty inputs, constant time series, and various anomaly scenarios.

---

## Contributing & License

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/xyz`).  
3. Write tests and code.  
4. Submit a Pull Request with a clear description.

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*For questions or support, contact the maintainer: adam.idris@live.co.uk
