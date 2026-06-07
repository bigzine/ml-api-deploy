import joblib
import pandas as pd
from huggingface_hub import hf_hub_download
import os

def load_model():
    """
    Télécharge et charge le modèle depuis Hugging Face Hub.
    Utilise le cache local si déjà téléchargé.
    """
    repo_id = os.getenv("HF_REPO_ID", "votre-username/ml-api-deploy")
    filename = os.getenv("HF_MODEL_FILENAME", "model.pkl")
    token = os.getenv("HF_TOKEN", None)  # Optionnel si repo public

    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        token=token
    )
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
    proba = model.predict_proba(features)[0][1]

    return {
        "prediction": int(prediction),
        "proba": float(proba)
    }
