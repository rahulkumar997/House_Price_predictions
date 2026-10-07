from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

TARGET_COLUMN = "median_house_value"
FEATURE_COLUMNS = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income",
    "ocean_proximity",
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "model.pkl"
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "housing.csv"


def _resolve_model_path(model_path: str | Path | None = None) -> Path:
    if model_path is None:
        return DEFAULT_MODEL_PATH
    return Path(model_path).resolve() if Path(model_path).is_absolute() else (Path.cwd() / model_path).resolve()


def _build_pipeline() -> Pipeline:
    numeric_features = [
        "longitude",
        "latitude",
        "housing_median_age",
        "total_rooms",
        "total_bedrooms",
        "population",
        "households",
        "median_income",
    ]
    categorical_features = ["ocean_proximity"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([("imputer", SimpleImputer(strategy="median"))]),
                numeric_features,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = HistGradientBoostingRegressor(
        learning_rate=0.05,
        max_depth=10,
        max_iter=500,
        random_state=42,
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def train_model(
    data_path: str | Path = DEFAULT_DATA_PATH,
    model_path: str | Path | None = None,
) -> Pipeline:
    data = pd.read_csv(data_path)
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"The target column '{TARGET_COLUMN}' was not found in {data_path}.")

    missing_features = [column for column in FEATURE_COLUMNS if column not in data.columns]
    if missing_features:
        raise ValueError(f"Missing required feature columns: {missing_features}")

    pipeline = _build_pipeline()
    pipeline.fit(data[FEATURE_COLUMNS], data[TARGET_COLUMN])

    resolved_path = _resolve_model_path(model_path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    with resolved_path.open("wb") as file_handle:
        pickle.dump(pipeline, file_handle)

    return pipeline


def load_model(model_path: str | Path | None = None) -> Pipeline:
    resolved_path = _resolve_model_path(model_path)
    if not resolved_path.exists():
        return train_model(model_path=resolved_path)

    with resolved_path.open("rb") as file_handle:
        return pickle.load(file_handle)


def predict_house_value(
    data: pd.DataFrame | dict[str, Any] | list[dict[str, Any]],
    model: Pipeline | None = None,
) -> pd.Series:
    if isinstance(data, dict):
        frame = pd.DataFrame([data])
    elif isinstance(data, list):
        frame = pd.DataFrame(data)
    else:
        frame = data.copy()

    missing_columns = [column for column in FEATURE_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Missing required feature columns: {missing_columns}")

    pipeline = model or load_model()
    predictions = pipeline.predict(frame[FEATURE_COLUMNS])
    return pd.Series(predictions, index=frame.index, name="predicted_price")
