from pydantic import BaseModel

class PredictionInput(BaseModel):
    features: list[float]

class PredictionOutput(BaseModel):
    prediction: float | str
    confidence: float | None = None
