import joblib
import pandas as pd
import os

def load_model(path: str = None):
    """Charge le modèle depuis le fichier local."""
    if path is None:
        path = os.getenv("MODEL_PATH", "models/model.pkl")
    return joblib.load(path)


def predict(model, features: pd.DataFrame) -> dict:
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]
    return {
        "prediction": int(prediction),
        "proba": float(proba)
    }