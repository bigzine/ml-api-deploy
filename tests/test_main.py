from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "ML API is running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_no_model():
    """Sans modèle chargé, l'API doit retourner 503"""
    payload = {
        "age": 35, "revenu_mensuel": 5000,
        "nombre_experiences_precedentes": 2,
        "annees_dans_l_entreprise": 7,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 2,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "nombre_participation_pee": 2,
        "nb_formations_suivies": 3,
        "distance_domicile_travail": 25,
        "niveau_education": 3,
        "frequence_deplacement": 2,
        "annees_depuis_la_derniere_promotion": 4,
        "augmentation_salaire_precedente": 8,
        "heure_supplementaires": 1,
        "genre_femme": 0, "genre_homme": 1,
        "statut_marital_celibataire": 1,
        "statut_marital_divorce": 0,
        "statut_marital_marie": 0,
        "departement_rh": 0, "departement_rd": 0,
        "departement_ventes": 1,
        "poste_consultant": 0, "poste_developpeur": 0,
        "poste_directeur": 0, "poste_manager": 0,
        "poste_technicien": 1,
        "domaine_etude_informatique": 1,
        "domaine_etude_marketing": 0,
        "domaine_etude_medical": 0,
        "domaine_etude_rh": 0,
        "domaine_etude_technique": 0,
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 503
