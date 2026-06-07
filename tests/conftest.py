"""
Configuration des tests - Mock du modèle et de la base de données
"""
import pytest
import numpy as np
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_db():
    """Mock de la base de données pour le CI."""
    fake_db = MagicMock()
    fake_db.add = MagicMock()
    fake_db.commit = MagicMock()
    fake_db.refresh = MagicMock()

    with patch("app.database.SessionLocal", return_value=fake_db), \
         patch("app.database.engine", MagicMock()), \
         patch("app.routers.predict.get_db", return_value=iter([fake_db])):
        yield fake_db


@pytest.fixture(autouse=True)
def mock_model():
    """Faux modèle sklearn pour les tests."""
    import app.routers.predict as predict_module

    fake_model = MagicMock()
    fake_model.predict.return_value = np.array([0])
    fake_model.predict_proba.return_value = np.array([[0.68, 0.32]])

    original_model = predict_module.model
    predict_module.model = fake_model

    yield fake_model

    predict_module.model = original_model
