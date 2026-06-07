from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import EmployeeInput, PredictionOutput
from app.model import load_model, predict
from app.database import get_db
from app.models_db import Prediction
import pandas as pd
import os

router = APIRouter(prefix="/predict", tags=["Prédiction"])

model = None

try:
    MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
    model = load_model(MODEL_PATH)
    print("Modèle chargé")
except Exception as e:
    print(f"Modèle non chargé : {e}")


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df['satisfaction_globale'] = (
        df['satisfaction_employee_environnement'] +
        df['satisfaction_employee_nature_travail'] +
        df['satisfaction_employee_equipe'] +
        df['satisfaction_employee_equilibre_pro_perso']
    ) / 4

    df['indicateur_surcharge'] = (
        (df['heure_supplementaires'] == 1) &
        (df['satisfaction_employee_equilibre_pro_perso'] <= 2)
    ).astype(int)

    return df


FEATURE_ORDER = [
    'age', 'revenu_mensuel', 'nombre_experiences_precedentes',
    'annees_dans_l_entreprise', 'satisfaction_employee_environnement',
    'note_evaluation_precedente', 'satisfaction_employee_nature_travail',
    'satisfaction_employee_equipe', 'satisfaction_employee_equilibre_pro_perso',
    'note_evaluation_actuelle', 'heure_supplementaires',
    'nombre_participation_pee', 'nb_formations_suivies',
    'distance_domicile_travail', 'niveau_education', 'frequence_deplacement',
    'annees_depuis_la_derniere_promotion', 'satisfaction_globale',
    'indicateur_surcharge', 'genre_M', 'departement_Consulting',
    'departement_Ressources Humaines', 'statut_marital_Divorcé(e)',
    'statut_marital_Marié(e)', 'domaine_etude_Entrepreunariat',
    'domaine_etude_Infra & Cloud', 'domaine_etude_Marketing',
    'domaine_etude_Ressources Humaines', 'domaine_etude_Transformation Digitale',
    'poste_Cadre Commercial', 'poste_Consultant', 'poste_Directeur Technique',
    'poste_Manager', 'poste_Représentant Commercial', 'poste_Ressources Humaines',
    'poste_Senior Manager', 'poste_Tech Lead'
]


@router.post("/", response_model=PredictionOutput, summary="Prédire l'attrition d'un employé")
def predict_attrition(employee: EmployeeInput, db: Session = Depends(get_db)):
    """
    Prédit si un employé va quitter l'entreprise.
    Les inputs et outputs sont enregistrés en base de données.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")

    data = employee.model_dump(by_alias=True)
    input_df = pd.DataFrame([data])
    input_df = add_engineered_features(input_df)
    input_df = input_df[FEATURE_ORDER]

    result = predict(model, input_df)

    # Enregistrement en base de données
    prediction_record = Prediction(
        input_data=data,
        prediction=int(result["prediction"]),
        label="Quitte l'entreprise" if result["prediction"] == 1 else "Reste dans l'entreprise",
        probabilite_depart=round(float(result["proba"]), 4),
        satisfaction_globale=round(float(input_df['satisfaction_globale'].iloc[0]), 4),
        indicateur_surcharge=int(input_df['indicateur_surcharge'].iloc[0]),
        model_version="0.1.0"
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return PredictionOutput(
        prediction=prediction_record.prediction,
        label=prediction_record.label,
        probabilite_depart=prediction_record.probabilite_depart
    )
