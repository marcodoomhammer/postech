from contextlib import asynccontextmanager
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from .config import MODEL_PATH
from .data import prepare_features
from .schemas import Customer, Prediction

def create_app(model_path: Path = MODEL_PATH):
    @asynccontextmanager
    async def lifespan(app):
        # Nunca treine no startup. Carregue somente artefatos de origem confiável.
        app.state.artifact = joblib.load(model_path) if model_path.exists() else None
        yield
        app.state.artifact = None

    app = FastAPI(title="Telco Churn API", version="1.0.0", lifespan=lifespan)

    @app.get("/health")
    def health(request: Request):
        ready = request.app.state.artifact is not None
        return {"status": "ok", "model_loaded": ready}

    @app.post("/predict", response_model=Prediction)
    def predict(customer: Customer, request: Request):
        artifact = request.app.state.artifact
        if artifact is None:
            raise HTTPException(status_code=503, detail="Modelo indisponível. Execute python -m churn.train e reinicie a API.")
        # O contrato valida a entrada; o pipeline aplica a transformação aprendida.
        # Não recalculamos mediana ou escala com os dados deste cliente.
        frame = prepare_features(pd.DataFrame([customer.model_dump()]))
        probability = float(artifact["pipeline"].predict_proba(frame)[0, 1])
        metadata = artifact["metadata"]
        return Prediction(churn_probability=probability,
            churn_prediction=int(probability >= metadata["threshold"]),
            threshold=metadata["threshold"], model_name=metadata["model_name"])
    return app

app = create_app()
