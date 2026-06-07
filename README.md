# ml-api-deploy

API REST de prédiction d'attrition des employés (Projet 4 - Classification RH).

## Description

Prédit si un employé va quitter l'entreprise à partir de 35 features RH.
Le modèle est hébergé sur **Hugging Face Hub** et téléchargé automatiquement au démarrage.

## Structure

```
ml-api-deploy/
├── app/
│   ├── main.py              # FastAPI entry point + chargement modèle
│   ├── model.py             # Chargement HF Hub + inférence
│   ├── schemas.py           # Schémas Pydantic (35 features)
│   └── routers/
│       └── predict.py       # Endpoint POST /predict
├── tests/
│   └── test_main.py
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copiez `.env.example` en `.env` et renseignez vos variables :

```bash
cp .env.example .env
```

```env
HF_REPO_ID=votre-username/ml-api-deploy
HF_MODEL_FILENAME=model.pkl
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx  # Optionnel si repo public
```

## Upload du modèle sur Hugging Face

Depuis votre notebook après entraînement :

```python
import joblib
from huggingface_hub import HfApi

joblib.dump(model, "model.pkl")

api = HfApi()
api.upload_file(
    path_or_fileobj="model.pkl",
    path_in_repo="model.pkl",
    repo_id="votre-username/ml-api-deploy",
    repo_type="model"
)
```

## Lancement

```bash
uvicorn app.main:app --reload
```

Swagger UI : http://localhost:8000/docs

## Endpoint principal

### `POST /predict/`

**Réponse** :
```json
{
  "prediction": 1,
  "label": "Quitte l'entreprise",
  "probabilite_depart": 0.82
}
```

## Tests

```bash
pytest tests/ --cov=app
```
