"""House price prediction package."""

from .model import (  # noqa: F401
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_model,
    predict_house_value,
    train_model,
)

__version__ = "0.1.0"