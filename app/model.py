import joblib
import pandas as pd
import numpy as np

def load_model(path: str):
    """Charge le modèle ML depuis un fichier .pkl"""
    return joblib.load(path)

def predict(model, features: pd.DataFrame) -> dict:
    """
    Effectue une prédiction d'attrition.

    Args:
        model: modèle sklearn chargé
        features: DataFrame avec les 35 features

    Returns:
        dict avec prediction (0/1) et proba
    """
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]  # Proba de quitter

    return {
        "prediction": int(prediction),
        "proba": float(proba)
    }
