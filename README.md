# ml-api-deploy

API REST de prédiction d'attrition des employés — Projet 4 (Classification RH).

Développé dans le cadre d'un projet de déploiement de modèle de machine learning en production, ce projet expose un modèle Random Forest via une API FastAPI, avec une base de données PostgreSQL pour la traçabilité, un pipeline CI/CD GitHub Actions, et un déploiement sur Hugging Face Spaces via Docker.

---

## Sommaire

- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement en local](#lancement-en-local)
- [Base de données](#base-de-données)
- [Endpoints API](#endpoints-api)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [CI/CD](#cicd)
- [Structure du projet](#structure-du-projet)

---

## Architecture

```
GitHub (code source)
    └── CI : tests automatiques sur chaque push
    └── CD : déploiement automatique sur HF Spaces (push sur main)

HF Spaces (API en production)
    └── Docker (FastAPI sur port 7860)
    └── Charge models/model.pkl au démarrage
    └── Expose POST /predict/

PostgreSQL (local)
    └── Table employees (1470 lignes)
    └── Table predictions (traçabilité inputs/outputs)
```

---

## Prérequis

- Python 3.11+
- PostgreSQL 18
- Git

---

## Installation

```bash
git clone https://github.com/Ediagabate/ml-api-deploy.git
cd ml-api-deploy
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Configuration

Copiez `.env.example` en `.env` et renseignez vos variables :

```env
DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/ml_api_db
MODEL_PATH=models/model.pkl
```

Placez votre modèle entraîné dans `models/model.pkl` :

```python
import joblib
joblib.dump(final_model, "models/model.pkl")
```

---

## Lancement en local

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur :
- Interface : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- Santé : http://localhost:8000/health

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

### Schéma

| Table | Description |
|---|---|
| `employees` | Dataset complet des 1470 employés |
| `predictions` | Historique des inputs/outputs du modèle |

---

## Endpoints API

### `GET /`
Retourne le statut de l'API.

```json
{"message": "ML API is running", "version": "0.1.0"}
```

### `GET /health`
Vérification de santé.

```json
{"status": "ok"}
```

### `POST /predict/`
Prédit si un employé va quitter l'entreprise.

**Body** : 35 features RH (voir Swagger pour la liste complète)

**Réponse** :
```json
{
  "prediction": 0,
  "label": "Reste dans l'entreprise",
  "probabilite_depart": 0.3222
}
```

**Exemple de requête** :
```python
import requests

payload = {
    "age": 35,
    "revenu_mensuel": 5000,
    "heure_supplementaires": 1,
    "satisfaction_employee_environnement": 3,
    ...
}

response = requests.post(
    "https://ediagabate-ml-api-deploy.hf.space/predict/",
    json=payload
)
print(response.json())
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
start htmlcov/index.html
```

### Types de tests

| Fichier | Type | Description |
|---|---|---|
| `test_main.py` | Unitaire | Endpoints `/` et `/health` |
| `test_predict.py` | Unitaire | Validation Pydantic, erreurs 422/503 |
| `test_features.py` | Unitaire | Feature engineering |
| `test_functional.py` | Fonctionnel | Tests avec le vrai modèle (local uniquement) |

**Résultats** : 30 tests ✅ — Couverture : 56%

---

## Déploiement

### Hugging Face Spaces

L'API est déployée sur HF Spaces via Docker :

```
https://ediagabate-ml-api-deploy.hf.space
```

### Docker local

```bash
docker build -t ml-api-deploy .
docker run -p 8000:7860 ml-api-deploy
```

### Docker Compose

```bash
docker-compose up
```

---

## CI/CD

### Pipeline CI (GitHub Actions)

Déclenché sur chaque push :
- Installation des dépendances
- Exécution des tests avec couverture
- Génération du rapport de couverture

### Pipeline CD (GitHub Actions)

Déclenché sur push vers `main` :
- Tests (gate avant déploiement)
- Déploiement automatique sur HF Spaces

### Secrets GitHub requis

| Secret | Description |
|---|---|
| `HF_TOKEN` | Token Hugging Face |
| `HF_SPACE_ID` | `Ediagabate/ml-api-deploy` |

---

## Structure du projet

```
ml-api-deploy/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── model.py             # Chargement et inférence
│   ├── schemas.py           # Validation Pydantic (35 features)
│   ├── database.py          # Connexion SQLAlchemy
│   ├── models_db.py         # Tables ORM
│   └── routers/
│       └── predict.py       # Endpoint POST /predict/
├── scripts/
│   ├── create_db.py         # Création des tables
│   ├── create_db.sql        # Script SQL de référence
│   ├── insert_dataset.py    # Insertion du dataset
│   └── deploy_to_hf.py      # Déploiement HF Spaces
├── tests/
│   ├── conftest.py          # Fixtures et mocks
│   ├── test_main.py         # Tests endpoints principaux
│   ├── test_predict.py      # Tests endpoint /predict/
│   ├── test_features.py     # Tests feature engineering
│   └── test_functional.py   # Tests fonctionnels (local)
├── models/
│   └── model.pkl            # Modèle Random Forest optimisé
├── .github/
│   └── workflows/
│       ├── ci.yml           # Pipeline CI
│       └── cd.yml           # Pipeline CD
├── Dockerfile               # Container Docker (port 7860)
├── docker-compose.yml       # Dev local
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## Modèle

Random Forest Classifier optimisé avec :
- `n_estimators=300`
- `max_depth=5`
- `min_samples_leaf=20`
- `max_features=0.5`
- `class_weight='balanced_subsample'`

Les features engineerées calculées automatiquement par l'API :
- `satisfaction_globale` : moyenne des 4 scores de satisfaction
- `indicateur_surcharge` : heures sup ET équilibre pro/perso ≤ 2
