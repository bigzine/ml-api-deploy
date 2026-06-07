from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Employee(Base):
    """Table des employés (dataset complet)"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Float, nullable=False)
    revenu_mensuel = Column(Float, nullable=False)
    nombre_experiences_precedentes = Column(Float)
    annees_dans_l_entreprise = Column(Float)
    satisfaction_employee_environnement = Column(Float)
    note_evaluation_precedente = Column(Float)
    note_evaluation_actuelle = Column(Float)
    satisfaction_employee_nature_travail = Column(Float)
    satisfaction_employee_equipe = Column(Float)
    satisfaction_employee_equilibre_pro_perso = Column(Float)
    heure_supplementaires = Column(Integer)
    nombre_participation_pee = Column(Float)
    nb_formations_suivies = Column(Float)
    distance_domicile_travail = Column(Float)
    niveau_education = Column(Float)
    frequence_deplacement = Column(Float)
    annees_depuis_la_derniere_promotion = Column(Float)
    genre = Column(String(10))
    departement = Column(String(50))
    statut_marital = Column(String(20))
    domaine_etude = Column(String(50))
    poste = Column(String(50))
    a_quitte_entreprise = Column(Integer, nullable=True)  # label réel

    predictions = relationship("Prediction", back_populates="employee")
    created_at = Column(DateTime, server_default=func.now())


class Prediction(Base):
    """Table des prédictions (inputs + outputs du modèle)"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Input complet envoyé au modèle
    input_data = Column(JSON, nullable=False)

    # Output du modèle
    prediction = Column(Integer, nullable=False)
    label = Column(String(50), nullable=False)
    probabilite_depart = Column(Float, nullable=False)

    # Features engineerées calculées
    satisfaction_globale = Column(Float)
    indicateur_surcharge = Column(Integer)

    # Métadonnées
    model_version = Column(String(20), default="0.1.0")
    created_at = Column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="predictions")
