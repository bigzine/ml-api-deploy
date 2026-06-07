"""
Tests fonctionnels - Scénarios réels avec le vrai modèle.
Ces tests nécessitent model.pkl et sont ignorés dans le CI.
"""
import pytest
import joblib
import os
import pandas as pd

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
MODEL_AVAILABLE = os.path.exists(MODEL_PATH)

pytestmark = pytest.mark.skipif(
    not MODEL_AVAILABLE,
    reason="model.pkl non disponible - tests fonctionnels ignorés en CI"
)


@pytest.fixture(scope="module")
def real_model():
    return joblib.load(MODEL_PATH)


def make_input(overrides: dict = {}) -> pd.DataFrame:
    """Crée un DataFrame avec des valeurs par défaut."""
    base = {
        'age': 35, 'revenu_mensuel': 5000,
        'nombre_experiences_precedentes': 2,
        'annees_dans_l_entreprise': 7,
        'satisfaction_employee_environnement': 3,
        'note_evaluation_precedente': 3,
        'satisfaction_employee_nature_travail': 2,
        'satisfaction_employee_equipe': 3,
        'satisfaction_employee_equilibre_pro_perso': 3,
        'note_evaluation_actuelle': 3,
        'heure_supplementaires': 0,
        'nombre_participation_pee': 2,
        'nb_formations_suivies': 3,
        'distance_domicile_travail': 10,
        'niveau_education': 3,
        'frequence_deplacement': 1,
        'annees_depuis_la_derniere_promotion': 2,
        'satisfaction_globale': 2.75,
        'indicateur_surcharge': 0,
        'genre_M': 1,
        'departement_Consulting': 0,
        'departement_Ressources Humaines': 0,
        'statut_marital_Divorcé(e)': 0,
        'statut_marital_Marié(e)': 1,
        'domaine_etude_Entrepreunariat': 0,
        'domaine_etude_Infra & Cloud': 0,
        'domaine_etude_Marketing': 0,
        'domaine_etude_Ressources Humaines': 0,
        'domaine_etude_Transformation Digitale': 1,
        'poste_Cadre Commercial': 0,
        'poste_Consultant': 0,
        'poste_Directeur Technique': 0,
        'poste_Manager': 1,
        'poste_Représentant Commercial': 0,
        'poste_Ressources Humaines': 0,
        'poste_Senior Manager': 0,
        'poste_Tech Lead': 0
    }
    base.update(overrides)
    return pd.DataFrame([base])


# ── Tests de base ────────────────────────────────────────────────
def test_model_loads(real_model):
    """Le modèle se charge correctement."""
    assert real_model is not None


def test_model_predict_returns_binary(real_model):
    """predict() retourne 0 ou 1."""
    df = make_input()
    result = real_model.predict(df)[0]
    assert result in [0, 1]


def test_model_proba_range(real_model):
    """predict_proba() retourne des valeurs entre 0 et 1."""
    df = make_input()
    proba = real_model.predict_proba(df)[0]
    assert all(0.0 <= p <= 1.0 for p in proba)
    assert abs(sum(proba) - 1.0) < 1e-6


def test_model_proba_sums_to_one(real_model):
    """Les probabilités somment à 1."""
    df = make_input()
    proba = real_model.predict_proba(df)[0]
    assert abs(sum(proba) - 1.0) < 1e-6


# ── Tests profils métier ─────────────────────────────────────────
def test_profil_faible_risque(real_model):
    """Employé satisfait sans heures sup → faible probabilité de départ."""
    df = make_input({
        'satisfaction_employee_environnement': 4,
        'satisfaction_employee_nature_travail': 4,
        'satisfaction_employee_equipe': 4,
        'satisfaction_employee_equilibre_pro_perso': 4,
        'satisfaction_globale': 4.0,
        'heure_supplementaires': 0,
        'indicateur_surcharge': 0,
        'revenu_mensuel': 8000,
        'annees_depuis_la_derniere_promotion': 1,
    })
    proba = real_model.predict_proba(df)[0][1]
    assert proba < 0.6, f"Probabilité trop élevée pour profil faible risque: {proba}"


def test_profil_haut_risque(real_model):
    """Employé insatisfait avec heures sup → probabilité élevée de départ."""
    df = make_input({
        'satisfaction_employee_environnement': 1,
        'satisfaction_employee_nature_travail': 1,
        'satisfaction_employee_equipe': 1,
        'satisfaction_employee_equilibre_pro_perso': 1,
        'satisfaction_globale': 1.0,
        'heure_supplementaires': 1,
        'indicateur_surcharge': 1,
        'revenu_mensuel': 2000,
        'annees_depuis_la_derniere_promotion': 10,
        'distance_domicile_travail': 50,
    })
    proba = real_model.predict_proba(df)[0][1]
    assert proba > 0.2, f"Probabilité trop faible pour profil haut risque: {proba}"


# ── Tests cas limites ────────────────────────────────────────────
def test_valeurs_minimales(real_model):
    """Le modèle gère les valeurs minimales sans erreur."""
    df = make_input({
        'age': 18, 'revenu_mensuel': 1000,
        'satisfaction_employee_environnement': 1,
        'satisfaction_employee_nature_travail': 1,
        'satisfaction_employee_equipe': 1,
        'satisfaction_employee_equilibre_pro_perso': 1,
        'satisfaction_globale': 1.0,
        'niveau_education': 1, 'frequence_deplacement': 0,
        'distance_domicile_travail': 1,
    })
    result = real_model.predict(df)[0]
    assert result in [0, 1]


def test_valeurs_maximales(real_model):
    """Le modèle gère les valeurs maximales sans erreur."""
    df = make_input({
        'age': 60, 'revenu_mensuel': 20000,
        'satisfaction_employee_environnement': 4,
        'satisfaction_employee_nature_travail': 4,
        'satisfaction_employee_equipe': 4,
        'satisfaction_employee_equilibre_pro_perso': 4,
        'satisfaction_globale': 4.0,
        'niveau_education': 5, 'frequence_deplacement': 2,
        'distance_domicile_travail': 100,
        'annees_depuis_la_derniere_promotion': 15,
    })
    result = real_model.predict(df)[0]
    assert result in [0, 1]


def test_reproductibilite(real_model):
    """Le modèle retourne le même résultat pour le même input."""
    df = make_input()
    result1 = real_model.predict(df)[0]
    result2 = real_model.predict(df)[0]
    assert result1 == result2


def test_batch_predictions(real_model):
    """Le modèle gère plusieurs prédictions en batch."""
    rows = [make_input({'age': age}).iloc[0] for age in [25, 35, 45, 55]]
    df = pd.DataFrame(rows)
    results = real_model.predict(df)
    assert len(results) == 4
    assert all(r in [0, 1] for r in results)
