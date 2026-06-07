from fastapi import FastAPI
from app.routers import predict
from app.model import load_model
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ml-api-deploy",
    description="API de prédiction d'attrition des employés (Projet 4)",
    version="0.1.0"
)

app.include_router(predict.router)

@app.on_event("startup")
async def startup_event():
    """Charge le modèle depuis Hugging Face au démarrage."""
    try:
        predict.model = load_model()
        logger.info("✅ Modèle chargé depuis Hugging Face")
    except Exception as e:
        logger.warning(f"⚠️ Modèle non chargé : {e}")

@app.get("/")
def root():
    return {"message": "ML API is running", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
