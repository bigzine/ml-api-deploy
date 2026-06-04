# ml-api-deploy

API REST pour exposer un modèle de Machine Learning avec FastAPI.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn app.main:app --reload
```

Docs disponibles sur : http://localhost:8000/docs

## Tests

```bash
pytest tests/ --cov=app
```
