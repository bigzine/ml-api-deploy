import pytest
import numpy as np
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_dependencies():
    fake_model = MagicMock()
    fake_model.predict.return_value = np.array([0])
    fake_model.predict_proba.return_value = np.array([[0.68, 0.32]])

    with patch("app.routers.predict.save_to_db", return_value=None), \
         patch("app.routers.predict.model", fake_model):
        yield fake_model