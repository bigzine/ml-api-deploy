from fastapi import FastAPI

app = FastAPI(
    title="ml-api-deploy",
    description="Machine Learning model exposed via REST API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "ML API is running", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
