# ml-api-deploy

API REST de prédiction d'attrition des employés — Projet 4 (Classification RH).

Ce projet expose un modèle Random Forest via FastAPI, avec une base de données PostgreSQL pour la traçabilité, un pipeline CI/CD GitHub Actions, et un déploiement sur Hugging Face Spaces via Docker.

---

## Sommaire

- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement en local](#lancement-en-local)
- [Authentification et sécurité](#authentification-et-sécurité)
- [Base de données](#base-de-données)
- [Endpoints API](#endpoints-api)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [CI/CD](#cicd)
- [Données analytiques](#données-analytiques)
- [Choix techniques](#choix-techniques)
- [Mise à jour du modèle](#mise-à-jour-du-modèle)
- [Structure du projet](#structure-du-projet)

---

## Architecture

```
GitHub (code source)
    └── CI : tests automatiques sur chaque push (toutes branches)
    └── CD : déploiement automatique sur HF Spaces (push sur main)

HF Spaces (API en production)
    └── Docker (FastAPI sur port 7860)
    └── Charge models/model.pkl au démarrage
    └── Expose POST /predict/
    └── Swagger : https://ediagabate-ml-api-deploy.hf.space/docs

PostgreSQL local
    └── Table employees (1470 lignes — dataset complet)
    └── Table predictions (traçabilité inputs/outputs du modèle)
```

---

## Installation

```bash
git clone https://github.com/Ediagabate/ml-api-deploy.git
cd ml-api-deploy
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Configuration

Copiez `.env.example` en `.env` :

```bash
cp .env.example .env
```

Renseignez les variables :

```env
# Environnement
ENV=development

# Base de données PostgreSQL
DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/ml_api_db

# Modèle ML
MODEL_PATH=models/model.pkl

# Hugging Face (pour le déploiement)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
HF_SPACE_ID=Ediagabate/ml-api-deploy
```

Placez votre modèle dans `models/model.pkl` :

```python
import joblib
joblib.dump(final_model, "models/model.pkl")
```

---

## Lancement en local

```bash
uvicorn app.main:app --reload
```

- Interface : http://localhost:8000
- Swagger : http://localhost:8000/docs
- Santé : http://localhost:8000/health

---

## Authentification et sécurité

### Gestion des secrets

Les secrets ne sont **jamais** committés dans Git :
- Variables sensibles dans `.env` (exclu par `.gitignore`)
- Secrets de déploiement dans GitHub Secrets (`HF_TOKEN`, `HF_SPACE_ID`)
- Mot de passe PostgreSQL dans `DATABASE_URL` via variable d'environnement

### Fichier `.gitignore`

Les fichiers sensibles sont exclus :
```
.env
.env.*
*.pkl
*.joblib
```

### Bonnes pratiques appliquées

- Aucun mot de passe ou token en dur dans le code
- `DATABASE_URL` chargée via `python-dotenv`
- Secrets CI/CD gérés via GitHub Secrets (chiffrés)
- Modèle `.pkl` exclu de Git (binaire potentiellement sensible)

### Authentification API (extension possible)

Pour sécuriser l'API en production, ajouter une clé API via header :

```python
from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Clé API invalide")
```

Appel sécurisé :
```python
requests.post(url, json=payload, headers={"X-API-Key": "votre-cle"})
```

---

## Base de données

### Création des tables

```bash
python scripts/create_db.py
```

### Insertion du dataset

```bash
python scripts/insert_dataset.py --csv data/employees.csv
```

### Schéma des tables

**`employees`** — Dataset des 1470 employés :

| Colonne | Type | Description |
|---|---|---|
| id | SERIAL PK | Identifiant unique |
| age | FLOAT | Âge de l'employé |
| revenu_mensuel | FLOAT | Revenu mensuel |
| departement | VARCHAR | Département |
| poste | VARCHAR | Poste occupé |
| a_quitte_entreprise | INTEGER | Label réel (0/1) |
| created_at | TIMESTAMP | Date d'insertion |

**`predictions`** — Traçabilité des prédictions :

| Colonne | Type | Description |
|---|---|---|
| id | SERIAL PK | Identifiant unique |
| employee_id | INTEGER FK | Lien vers employees |
| input_data | JSONB | Features envoyées au modèle |
| prediction | INTEGER | 0=reste, 1=quitte |
| label | VARCHAR | Libellé lisible |
| probabilite_depart | FLOAT | Score de probabilité |
| satisfaction_globale | FLOAT | Feature engineerée |
| indicateur_surcharge | INTEGER | Feature engineerée |
| model_version | VARCHAR | Version du modèle |
| created_at | TIMESTAMP | Horodatage |

### Requêtes utiles

```sql
-- Dernières prédictions
SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10;

-- Taux de départ prédit
SELECT
    prediction,
    COUNT(*) as nb,
    ROUND(AVG(probabilite_depart)::numeric, 3) as proba_moyenne
FROM predictions
GROUP BY prediction;

-- Prédictions par département
SELECT e.departement, COUNT(*) as nb_predictions, AVG(p.probabilite_depart) as risque_moyen
FROM predictions p
JOIN employees e ON p.employee_id = e.id
GROUP BY e.departement
ORDER BY risque_moyen DESC;
```

---

## Endpoints API

### `GET /`
```json
{"message": "ML API is running", "version": "0.1.0"}
```

### `GET /health`
```json
{"status": "ok"}
```

### `POST /predict/`

Prédit si un employé va quitter l'entreprise.

**Body** (35 features) :
```json
{
  "age": 35,
  "revenu_mensuel": 5000,
  "satisfaction_employee_environnement": 3,
  "heure_supplementaires": 1,
  "genre_M": 1,
  "departement_Consulting": 0,
  "poste_Manager": 1,
  ...
}
```

**Réponse** :
```json
{
  "prediction": 0,
  "label": "Reste dans l'entreprise",
  "probabilite_depart": 0.3222
}
```

**Erreurs** :
- `422` — données invalides (Pydantic)
- `503` — modèle non disponible

La documentation complète avec tous les champs est disponible sur le Swagger :
```
https://ediagabate-ml-api-deploy.hf.space/docs
```

---

## Tests

### Lancer tous les tests

```bash
pytest tests/ -v
```

### Rapport de couverture

```bash
pytest tests/ --cov=app --cov-report=html
start htmlcov/index.html   # Windows
```

### Types de tests

| Fichier | Type | Environnement |
|---|---|---|
| `test_main.py` | Unitaire | CI + Local |
| `test_predict.py` | Unitaire | CI + Local |
| `test_features.py` | Unitaire | CI + Local |
| `test_functional.py` | Fonctionnel | Local uniquement |

**Résultats** : 30 tests ✅ — Couverture globale : 56%

| Module | Couverture |
|---|---|
| `app/main.py` | 100% |
| `app/schemas.py` | 100% |
| `app/model.py` | 91% |
| `app/routers/predict.py` | 70% |

---

## Déploiement

### Hugging Face Spaces (production)

```
https://ediagabate-ml-api-deploy.hf.space
https://ediagabate-ml-api-deploy.hf.space/docs
```

### Docker local

```bash
docker build -t ml-api-deploy .
docker run -p 8000:7860 --env-file .env ml-api-deploy
```

### Docker Compose

```bash
docker-compose up
```

---

## CI/CD

### Pipeline CI — tests automatiques

Déclenché sur **chaque push** (toutes branches) et **PR** vers `main` :
1. Installation des dépendances
2. Exécution des tests avec couverture
3. Génération du rapport XML

### Pipeline CD — déploiement automatique

Déclenché sur **push vers `main`** :
1. Tests (gate avant déploiement)
2. Déploiement automatique sur HF Spaces

### Gestion des environnements

| Environnement | Branche | Base de données |
|---|---|---|
| Développement | toutes | PostgreSQL local |
| Test (CI) | toutes | Mockée |
| Production | main | HF Spaces (sans DB) |

### Secrets GitHub requis

| Secret | Description |
|---|---|
| `HF_TOKEN` | Token Hugging Face (accès en écriture) |
| `HF_SPACE_ID` | `Ediagabate/ml-api-deploy` |

---

## Données analytiques

### Tableau de bord possible

Les données en base permettent de construire un tableau de bord RH :

```sql
-- Évolution du risque dans le temps
SELECT
    DATE_TRUNC('day', created_at) as jour,
    AVG(probabilite_depart) as risque_moyen,
    COUNT(*) as nb_predictions
FROM predictions
GROUP BY jour
ORDER BY jour;

-- Employés à haut risque
SELECT input_data->>'departement_Consulting' as dept,
       probabilite_depart
FROM predictions
WHERE probabilite_depart > 0.7
ORDER BY probabilite_depart DESC;
```

Ces requêtes peuvent alimenter un outil BI (Metabase, PowerBI, Tableau) connecté à PostgreSQL.

---

## Choix techniques

| Choix | Justification |
|---|---|
| **FastAPI** | Performance, documentation Swagger automatique, validation Pydantic native |
| **PostgreSQL** | Robustesse, support JSONB pour stocker les inputs du modèle, requêtes analytiques |
| **SQLAlchemy** | ORM Pythonique, migrations facilitées, abstraction de la DB |
| **Docker** | Reproductibilité, compatibilité HF Spaces, isolation des dépendances |
| **GitHub Actions** | Intégration native GitHub, gratuit, écosystème riche |
| **HF Spaces** | Hébergement gratuit, support Docker natif, visibilité communauté ML |
| **Random Forest** | Interprétabilité, robustesse au déséquilibre de classes, pas de normalisation requise |
| **Mocks dans les tests** | CI sans infrastructure (pas de DB, pas de modèle), tests rapides et reproductibles |

---

## Mise à jour du modèle

Pour remplacer le modèle en production :

1. Réentraîner dans le notebook
2. Exporter :
```python
import joblib
joblib.dump(new_model, "models/model.pkl")
```
3. Committer et pusher sur `main`
4. Le pipeline CD redéploie automatiquement

Versionnez les modèles avec des tags Git :
```bash
git tag -a v1.1.0 -m "Modèle réentraîné avec données 2026"
git push origin v1.1.0
```

---

## Structure du projet

```
ml-api-deploy/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── model.py             # Chargement et inférence ML
│   ├── schemas.py           # Validation Pydantic (35 features)
│   ├── database.py          # Connexion SQLAlchemy
│   ├── models_db.py         # Modèles ORM (employees, predictions)
│   └── routers/
│       └── predict.py       # Endpoint POST /predict/
├── scripts/
│   ├── create_db.py         # Création des tables (Python)
│   ├── create_db.sql        # Création des tables (SQL)
│   ├── insert_dataset.py    # Insertion du dataset CSV
│   └── deploy_to_hf.py      # Déploiement HF Spaces
├── tests/
│   ├── conftest.py          # Fixtures et mocks CI
│   ├── test_main.py         # Tests endpoints /  et /health
│   ├── test_predict.py      # Tests endpoint /predict/
│   ├── test_features.py     # Tests feature engineering
│   └── test_functional.py   # Tests fonctionnels (local)
├── models/
│   └── model.pkl            # Random Forest optimisé
├── .github/
│   └── workflows/
│       ├── ci.yml           # Pipeline CI (tests)
│       └── cd.yml           # Pipeline CD (déploiement)
├── Dockerfile               # Container Docker (port 7860)
├── docker-compose.yml       # Dev local
├── requirements.txt         # Dépendances Python
├── pytest.ini               # Configuration tests
├── .env.example             # Template variables d'environnement
├── .gitignore               # Fichiers exclus de Git
└── README.md                # Ce fichier
```
