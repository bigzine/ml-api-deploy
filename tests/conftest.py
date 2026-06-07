"""
Configuration des tests - Création d'un faux modèle pour le CI
"""
import pytest
import numpy as np
from unittest.mock import MagicMock
import app.routers.predict as predict_module


@pytest.fixture(autouse=True)
def mock_model():
    """
    Crée un faux modèle sklearn pour tous les tests.
    Evite d'avoir besoin du vrai model.pkl dans le CI.
    """
    fake_model = MagicMock()
    fake_model.predict.return_value = np.array([0])
    fake_model.predict_proba.return_value = np.array([[0.68, 0.32]])

    original_model = predict_module.model
    predict_module.model = fake_model

    yield fake_model

    predict_module.model = original_model
