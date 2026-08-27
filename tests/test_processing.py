import os
import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.processing import load_data

TITANIC_COLUMNS = [
    'PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 
    'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 
    'Cabin', 'Embarked'
]


@pytest.fixture
def mock_titanic_data():
    data = {
    'PassengerId': [1, 2],
    'Survived': [0, 1],
    'Pclass': [3, 1],
    'Name': ['Mr. A', 'Mrs. B'],
    'Sex': ['male', 'female'],
    'Age': [22.0, 38.0],
    "SibSp": [1, 38],
    "Parch": [0, 1],
    "Ticket": ["a", "b"],
    "Fare": [3.25, 3.14],
    "Cabin": ["D33", "C85"],
    "Embarked": ["S", "C"]
}
    return pd.DataFrame(data)

@pytest.fixture
def mock_config():
    mock_cfg = MagicMock()
    mock_cfg.data.path.raw = "data/raw/titanic.csv"
    return mock_cfg


def test_load_data_instance(mock_titanic_data, mock_config):
    with patch("pandas.read_csv", return_value=mock_titanic_data):
        dataframe = load_data(mock_config)

        print(dataframe.shape, flush=True)

        assert len(dataframe) == 2


