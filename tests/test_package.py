import pandas as pd

from house_price_prediction import __version__, load_model, predict_house_value


def test_package_version_is_defined():
    assert __version__ == "0.1.0"


def test_model_can_predict_for_a_valid_row():
    row = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41,
        "total_rooms": 880,
        "total_bedrooms": 129,
        "population": 322,
        "households": 126,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY",
    }

    model = load_model()
    prediction = predict_house_value(pd.DataFrame([row]), model=model)

    assert prediction.iloc[0] > 0
    assert len(prediction) == 1