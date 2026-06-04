from pydantic import BaseModel, Field, model_validator
from typing import Self

class EmployeeInput(BaseModel):
    # Variables numériques continues
    age: float = Field(..., example=35)
    revenu_mensuel: float = Field(..., example=5000)
    nombre_experiences_precedentes: float = Field(..., example=2)
    annees_dans_l_entreprise: float = Field(..., example=7)
    satisfaction_employee_environnement: float = Field(..., ge=1, le=4, example=3)
    note_evaluation_precedente: float = Field(..., ge=1, le=4, example=3)
    note_evaluation_actuelle: float = Field(..., ge=1, le=4, example=3)
    satisfaction_employee_nature_travail: float = Field(..., ge=1, le=4, example=2)
    satisfaction_employee_equipe: float = Field(..., ge=1, le=4, example=3)
    satisfaction_employee_equilibre_pro_perso: float = Field(..., ge=1, le=4, example=1)
    heure_supplementaires: int = Field(..., ge=0, le=1, example=1)
    nombre_participation_pee: float = Field(..., example=2)
    nb_formations_suivies: float = Field(..., example=3)
    distance_domicile_travail: float = Field(..., example=25)
    niveau_education: float = Field(..., ge=1, le=5, example=3)
    frequence_deplacement: float = Field(..., ge=0, le=2, example=1)
    annees_depuis_la_derniere_promotion: float = Field(..., example=2)

    # Genre
    genre_M: int = Field(..., ge=0, le=1, example=1)

    # Département
    departement_Consulting: int = Field(..., ge=0, le=1, example=0)
    departement_Ressources_Humaines: int = Field(..., ge=0, le=1, example=0, alias="departement_Ressources Humaines")

    # Statut marital
    statut_marital_Divorce: int = Field(..., ge=0, le=1, example=0, alias="statut_marital_Divorcé(e)")
    statut_marital_Marie: int = Field(..., ge=0, le=1, example=1, alias="statut_marital_Marié(e)")

    # Domaine étude
    domaine_etude_Entrepreunariat: int = Field(..., ge=0, le=1, example=0)
    domaine_etude_Infra_Cloud: int = Field(..., ge=0, le=1, example=0, alias="domaine_etude_Infra & Cloud")
    domaine_etude_Marketing: int = Field(..., ge=0, le=1, example=0)
    domaine_etude_Ressources_Humaines: int = Field(..., ge=0, le=1, example=0, alias="domaine_etude_Ressources Humaines")
    domaine_etude_Transformation_Digitale: int = Field(..., ge=0, le=1, example=1, alias="domaine_etude_Transformation Digitale")

    # Poste
    poste_Cadre_Commercial: int = Field(..., ge=0, le=1, example=0, alias="poste_Cadre Commercial")
    poste_Consultant: int = Field(..., ge=0, le=1, example=0)
    poste_Directeur_Technique: int = Field(..., ge=0, le=1, example=0, alias="poste_Directeur Technique")
    poste_Manager: int = Field(..., ge=0, le=1, example=1)
    poste_Representant_Commercial: int = Field(..., ge=0, le=1, example=0, alias="poste_Représentant Commercial")
    poste_Ressources_Humaines: int = Field(..., ge=0, le=1, example=0, alias="poste_Ressources Humaines")
    poste_Senior_Manager: int = Field(..., ge=0, le=1, example=0, alias="poste_Senior Manager")
    poste_Tech_Lead: int = Field(..., ge=0, le=1, example=0, alias="poste_Tech Lead")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
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
        }
    }


class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="0 = Reste, 1 = Quitte l'entreprise")
    label: str = Field(..., description="Libellé de la prédiction")
    probabilite_depart: float = Field(..., description="Probabilité de quitter l'entreprise")
