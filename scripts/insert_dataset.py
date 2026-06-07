"""
Insère le dataset complet dans la table employees.
Usage: python scripts/insert_dataset.py --csv data/employees.csv
"""
import sys
import os
import argparse
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(encoding='utf-8')

from app.database import SessionLocal
from app.models_db import Employee


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et convertit les colonnes avant insertion."""

    # Oui/Non → 1/0
    oui_non_cols = ['a_quitte_l_entreprise', 'heure_supplementaires']
    for col in oui_non_cols:
        if col in df.columns:
            df[col] = df[col].map({'Oui': 1, 'Non': 0, 'Yes': 1, 'No': 0})

    # Fréquence déplacement → numérique
    if 'frequence_deplacement' in df.columns:
        df['frequence_deplacement'] = df['frequence_deplacement'].map({
            'Non': 0, 'Occasionnel': 1, 'Frequent': 2,
            'Rarely': 0, 'Sometimes': 1, 'Frequently': 2
        })

    # Pourcentage augmentation → numérique
    if 'augementation_salaire_precedente' in df.columns:
        df['augementation_salaire_precedente'] = df['augementation_salaire_precedente']\
            .astype(str).str.replace('%', '').str.strip().astype(float)

    return df


def insert_dataset(csv_path: str):
    df = pd.read_csv(csv_path)
    df = clean_dataset(df)

    db = SessionLocal()
    count = 0

    try:
        for _, row in df.iterrows():
            employee = Employee(
                age=row.get("age"),
                revenu_mensuel=row.get("revenu_mensuel"),
                nombre_experiences_precedentes=row.get("nombre_experiences_precedentes"),
                annees_dans_l_entreprise=row.get("annees_dans_l_entreprise"),
                satisfaction_employee_environnement=row.get("satisfaction_employee_environnement"),
                note_evaluation_precedente=row.get("note_evaluation_precedente"),
                note_evaluation_actuelle=row.get("note_evaluation_actuelle"),
                satisfaction_employee_nature_travail=row.get("satisfaction_employee_nature_travail"),
                satisfaction_employee_equipe=row.get("satisfaction_employee_equipe"),
                satisfaction_employee_equilibre_pro_perso=row.get("satisfaction_employee_equilibre_pro_perso"),
                heure_supplementaires=row.get("heure_supplementaires"),
                nombre_participation_pee=row.get("nombre_participation_pee"),
                nb_formations_suivies=row.get("nb_formations_suivies"),
                distance_domicile_travail=row.get("distance_domicile_travail"),
                niveau_education=row.get("niveau_education"),
                frequence_deplacement=row.get("frequence_deplacement"),
                annees_depuis_la_derniere_promotion=row.get("annees_depuis_la_derniere_promotion"),
                genre=row.get("genre"),
                departement=row.get("departement"),
                statut_marital=row.get("statut_marital"),
                domaine_etude=row.get("domaine_etude"),
                poste=row.get("poste"),
                a_quitte_entreprise=row.get("a_quitte_l_entreprise"),
            )
            db.add(employee)
            count += 1

        db.commit()
        print(f"{count} employés insérés avec succès !")
    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Chemin vers le CSV du dataset")
    args = parser.parse_args()
    insert_dataset(args.csv)
