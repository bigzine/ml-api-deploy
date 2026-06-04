from fastapi import FastAPI
from app.routers import predict

app = FastAPI(
    title="ml-api-deploy",
    description="API de prédiction d'attrition des employés (Projet 4)",
    version="0.1.0"
)

app.include_router(predict.router)

@app.get("/")
def root():
    return {"message": "ML API is running", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
