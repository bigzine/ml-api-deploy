"""
Tests unitaires - Endpoints principaux
"""
from fastapi.testclient import TestClient
from app.main import app
import app.routers.predict as predict_module

client = TestClient(app)

VALID_PAYLOAD = {
    "age": 35,
    "revenu_mensuel": 5000,
    "nombre_experiences_precedentes": 2,
    "annees_dans_l_entreprise": 7,
    "satisfaction_employee_environnement": 3,
    "note_evaluation_precedente": 3,
    "note_evaluation_actuelle": 3,
    "satisfaction_employee_nature_travail": 2,
    "satisfaction_employee_equipe": 3,
    "satisfaction_employee_equilibre_pro_perso": 1,
    "heure_supplementaires": 1,
    "nombre_participation_pee": 2,
    "nb_formations_suivies": 3,
    "distance_domicile_travail": 25,
    "niveau_education": 3,
    "frequence_deplacement": 2,
    "annees_depuis_la_derniere_promotion": 4,
    "genre_M": 1,
    "departement_Consulting": 0,
    "departement_Ressources Humaines": 0,
    "statut_marital_Divorcé(e)": 0,
    "statut_marital_Marié(e)": 1,
    "domaine_etude_Entrepreunariat": 0,
    "domaine_etude_Infra & Cloud": 0,
    "domaine_etude_Marketing": 0,
    "domaine_etude_Ressources Humaines": 0,
    "domaine_etude_Transformation Digitale": 1,
    "poste_Cadre Commercial": 0,
    "poste_Consultant": 0,
    "poste_Directeur Technique": 0,
    "poste_Manager": 1,
    "poste_Représentant Commercial": 0,
    "poste_Ressources Humaines": 0,
    "poste_Senior Manager": 0,
    "poste_Tech Lead": 0
}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "ML API is running"
    assert "version" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_no_model():
    """Sans modèle chargé, l'API doit retourner 503"""
    original_model = predict_module.model
    predict_module.model = None

    try:
        response = client.post("/predict/", json=VALID_PAYLOAD)
        assert response.status_code == 503
    finally:
        predict_module.model = original_model
