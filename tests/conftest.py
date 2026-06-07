import pytest
import numpy as np
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_dependencies():
    fake_model = MagicMock()
    fake_model.predict.return_value = np.array([0])
    fake_model.predict_proba.return_value = np.array([[0.68, 0.32]])

    fake_db = MagicMock()
    fake_db.add = MagicMock()
    fake_db.commit = MagicMock()
    fake_db.refresh = MagicMock()

    with patch.dict('sys.modules', {
        'app.database': MagicMock(
            get_db=MagicMock(return_value=iter([fake_db])),
            engine=MagicMock(),
            SessionLocal=MagicMock(return_value=fake_db),
            Base=MagicMock()
        ),
        'app.models_db': MagicMock()
    }):
        import app.routers.predict as predict_module
        original_model = predict_module.model
        predict_module.model = fake_model

        yield

        predict_module.model = original_model