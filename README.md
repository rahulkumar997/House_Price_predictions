# House Price Prediction

A Python project for exploring housing data and building house-price prediction models.

## Getting started

Activate the virtual environment from the project root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and its dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the test suite:

```powershell
python -m pytest
```

## Project layout

```text
data/
  raw/          Original datasets (not tracked by Git)
  processed/    Cleaned or transformed datasets (not tracked by Git)
models/         Saved model artifacts (not tracked by Git)
notebooks/      Exploratory analysis notebooks
reports/figures Generated charts and figures (not tracked by Git)
src/house_price_prediction/  Python package source
tests/          Automated tests
```

Put source datasets in `data/raw/`. Keep large or sensitive datasets out of version control. Add the dataset's source and usage terms to your project notes before sharing results.

## Development

Install the project in editable mode with `python -m pip install -r requirements.txt`. This makes the `src/house_price_prediction` package importable while you work. Add data-specific loading, preprocessing, training, and evaluation code once the dataset and target column are selected.