"""
Tests unitaires - Feature engineering
"""
import pandas as pd
import pytest
from app.routers.predict import add_engineered_features


def test_satisfaction_globale_calcul():
    """satisfaction_globale = moyenne des 4 scores"""
    df = pd.DataFrame([{
        "satisfaction_employee_environnement": 4,
        "satisfaction_employee_nature_travail": 2,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "heure_supplementaires": 0
    }])
    df = add_engineered_features(df)
    assert df["satisfaction_globale"].iloc[0] == pytest.approx(3.0)


def test_indicateur_surcharge_actif():
    """indicateur_surcharge = 1 si HS=1 ET équilibre <= 2"""
    df = pd.DataFrame([{
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 2,
        "heure_supplementaires": 1
    }])
    df = add_engineered_features(df)
    assert df["indicateur_surcharge"].iloc[0] == 1


def test_indicateur_surcharge_inactif():
    """indicateur_surcharge = 0 si pas de HS"""
    df = pd.DataFrame([{
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "heure_supplementaires": 0
    }])
    df = add_engineered_features(df)
    assert df["indicateur_surcharge"].iloc[0] == 0


def test_indicateur_surcharge_equilibre_eleve():
    """indicateur_surcharge = 0 si HS=1 mais équilibre > 2"""
    df = pd.DataFrame([{
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "heure_supplementaires": 1
    }])
    df = add_engineered_features(df)
    assert df["indicateur_surcharge"].iloc[0] == 0
