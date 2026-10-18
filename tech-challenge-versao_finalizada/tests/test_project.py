import json
from pathlib import Path
import joblib
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression
from churn.config import ROOT, DATA_PATH, NUMERIC
from churn.data import prepare_features, load_data
from churn.pipeline import build_pipeline
from churn.api import create_app

@pytest.fixture
def payload():
    return json.loads((ROOT / "docs/example_customer.json").read_text())

@pytest.fixture(scope="module")
def artifact(tmp_path_factory):
    X, y = load_data()
    # Artefato independente: testes não dependem do campeão pré-treinado.
    pipeline = build_pipeline(LogisticRegression(max_iter=1000, random_state=42))
    pipeline.fit(X.iloc[:400], y.iloc[:400])
    path = tmp_path_factory.mktemp("model") / "test.joblib"
    joblib.dump({"pipeline": pipeline, "metadata": {"threshold": 0.5, "model_name": "test"}}, path)
    return path

def test_cleaning_drops_target_and_id_without_mutating(payload):
    frame = pd.DataFrame([{**payload, "TotalCharges": " ", "Churn": "Yes", "customerID": "x"}])
    clean = prepare_features(frame)
    assert pd.isna(clean.iloc[0]["TotalCharges"])
    assert "Churn" not in clean and "customerID" not in clean
    assert frame.iloc[0]["TotalCharges"] == " "

def test_missing_column(payload):
    del payload["tenure"]
    with pytest.raises(ValueError, match="tenure"):
        prepare_features(pd.DataFrame([payload]))

def test_health_without_model(tmp_path):
    with TestClient(create_app(tmp_path / "missing.joblib")) as client:
        assert client.get("/health").json() == {"status": "ok", "model_loaded": False}

def test_predict_unavailable(tmp_path, payload):
    with TestClient(create_app(tmp_path / "missing.joblib")) as client:
        assert client.post("/predict", json=payload).status_code == 503

def test_predict_pipeline_and_validation(artifact, payload):
    with TestClient(create_app(artifact)) as client:
        assert client.get("/health").json()["model_loaded"] is True
        result = client.post("/predict", json=payload)
        assert result.status_code == 200
        body = result.json()
        assert 0 <= body["churn_probability"] <= 1
        assert body["churn_prediction"] == int(body["churn_probability"] >= 0.5)
        assert client.post("/predict", json={**payload, "tenure": -1}).status_code == 422
        assert client.post("/predict", json={**payload, "Contract": "invalid"}).status_code == 422
        assert client.post("/predict", json={**payload, "Churn": "Yes"}).status_code == 422
        assert client.post("/predict", json={**payload, "PhoneService": "Yes"}).status_code == 422

def test_missing_total_charges_is_imputed(artifact, payload):
    payload.pop("TotalCharges")
    with TestClient(create_app(artifact)) as client:
        assert client.post("/predict", json=payload).status_code == 200


def test_imputer_uses_training_median(artifact, payload):
    # O status 200 não prova qual valor foi usado. Aqui olhamos a transformação.
    trained = joblib.load(artifact)["pipeline"]
    X, _ = load_data()
    expected = X.iloc[:400][NUMERIC].median().to_numpy()
    numeric = trained.named_steps["preprocess"].named_transformers_["numeric"]
    import numpy as np
    np.testing.assert_allclose(numeric.named_steps["impute"].statistics_, expected)
    payload["TotalCharges"] = None
    cleaned = prepare_features(pd.DataFrame([payload]))
    transformed = numeric.named_steps["impute"].transform(cleaned[NUMERIC])
    index = NUMERIC.index("TotalCharges")
    assert transformed[0, index] == pytest.approx(expected[index])


@pytest.mark.parametrize("field,value", [
    ("tenure", -1),
    ("MonthlyCharges", -0.01),
    ("TotalCharges", -1),
    ("Contract", "Contrato inexistente"),
])
def test_invalid_inputs_report_the_field(artifact, payload, field, value):
    with TestClient(create_app(artifact)) as client:
        response = client.post("/predict", json={**payload, field: value})
        assert response.status_code == 422
        assert any(field in error["loc"] for error in response.json()["detail"])


def test_missing_tenure_is_rejected_by_api(artifact, payload):
    payload.pop("tenure")
    with TestClient(create_app(artifact)) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        assert any("tenure" in error["loc"] for error in response.json()["detail"])


def test_internet_services_must_be_consistent(artifact, payload):
    payload.update(InternetService="No", OnlineSecurity="Yes")
    with TestClient(create_app(artifact)) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        assert "incompatível" in response.json()["detail"][0]["msg"]
