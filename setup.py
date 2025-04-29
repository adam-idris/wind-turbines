from setuptools import setup, find_packages

setup(
    name="wind_turbine_pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "pytest"
    ],
)