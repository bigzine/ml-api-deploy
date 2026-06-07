"""
Tests unitaires - Endpoint /predict
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ── Payload valide de référence ─────────────────────────────────
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


# ── Tests réponse valide ────────────────────────────────────────
def test_predict_valid_payload():
    """Un payload valide doit retourner 200"""
    response = client.post("/predict/", json=VALID_PAYLOAD)
    assert response.status_code == 200


def test_predict_response_structure():
    """La réponse doit contenir prediction, label, probabilite_depart"""
    response = client.post("/predict/", json=VALID_PAYLOAD)
    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert "probabilite_depart" in data


def test_predict_prediction_is_binary():
    """prediction doit être 0 ou 1"""
    response = client.post("/predict/", json=VALID_PAYLOAD)
    assert response.json()["prediction"] in [0, 1]


def test_predict_probability_range():
    """probabilite_depart doit être entre 0 et 1"""
    response = client.post("/predict/", json=VALID_PAYLOAD)
    proba = response.json()["probabilite_depart"]
    assert 0.0 <= proba <= 1.0


def test_predict_label_coherence():
    """Le label doit correspondre à la prediction"""
    response = client.post("/predict/", json=VALID_PAYLOAD)
    data = response.json()
    if data["prediction"] == 1:
        assert data["label"] == "Quitte l'entreprise"
    else:
        assert data["label"] == "Reste dans l'entreprise"


# ── Tests profil à risque élevé ─────────────────────────────────
def test_predict_high_risk_profile():
    """Un profil à risque élevé doit avoir une probabilité > 0.5"""
    high_risk = VALID_PAYLOAD.copy()
    high_risk.update({
        "heure_supplementaires": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "satisfaction_employee_environnement": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 1,
        "distance_domicile_travail": 50,
        "annees_depuis_la_derniere_promotion": 10,
    })
    response = client.post("/predict/", json=high_risk)
    assert response.status_code == 200


# ── Tests validation Pydantic ───────────────────────────────────
def test_predict_missing_field():
    """Un champ manquant doit retourner 422"""
    payload = VALID_PAYLOAD.copy()
    del payload["age"]
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422


def test_predict_invalid_satisfaction_range():
    """satisfaction hors [1-4] doit retourner 422"""
    payload = VALID_PAYLOAD.copy()
    payload["satisfaction_employee_environnement"] = 99
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422


def test_predict_invalid_heure_sup():
    """heure_supplementaires hors [0-1] doit retourner 422"""
    payload = VALID_PAYLOAD.copy()
    payload["heure_supplementaires"] = 5
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422


def test_predict_empty_payload():
    """Un payload vide doit retourner 422"""
    response = client.post("/predict/", json={})
    assert response.status_code == 422


def test_predict_wrong_type():
    """Un type incorrect doit retourner 422"""
    payload = VALID_PAYLOAD.copy()
    payload["age"] = "trente-cinq"
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422
