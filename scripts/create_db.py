"""
Script de création de la base de données PostgreSQL.
Usage: python scripts/create_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app import models_db  # noqa: F401 - nécessaire pour enregistrer les modèles

def create_tables():
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")
    print("  - employees")
    print("  - predictions")

if __name__ == "__main__":
    create_tables()
