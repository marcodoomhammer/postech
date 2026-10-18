"""Execute: python -m churn.train. Seleção exclusivamente por ROC-AUC de CV."""
import hashlib
import json
import platform
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import (roc_auc_score, average_precision_score, f1_score,
    precision_score, recall_score, accuracy_score, confusion_matrix)
from threadpoolctl import threadpool_limits
from .config import ROOT, DATA_PATH, MODEL_PATH, SEED, FEATURES
from .data import load_data
from .pipeline import candidates

def evaluate(y, probability, threshold=0.5):
    pred = (probability >= threshold).astype(int)
    k = max(1, int(np.ceil(len(y) * 0.2)))
    top = np.argsort(-probability, kind="stable")[:k]
    return {
        "roc_auc": float(roc_auc_score(y, probability)),
        "average_precision": float(average_precision_score(y, probability)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "accuracy": float(accuracy_score(y, pred)),
        "recall_at_top_20_percent": float(np.asarray(y)[top].sum() / np.asarray(y).sum()),
        "precision_at_top_20_percent": float(np.asarray(y)[top].mean()),
        "confusion_matrix_tn_fp_fn_tp": confusion_matrix(y, pred, labels=[0, 1]).ravel().tolist(),
    }

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    # Reservamos o teste antes de comparar os candidatos. Só o campeão o utiliza.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    models = candidates()
    rows = []
    for name, model in models.items():
        print(f"Validação cruzada: {name}", flush=True)
        with threadpool_limits(limits=1):
            result = cross_validate(model, X_train, y_train, cv=cv, n_jobs=1,
                scoring={"roc_auc": "roc_auc", "f1": "f1", "recall": "recall", "precision": "precision"},
                error_score="raise")
        row = {"model": name}
        for metric in ["roc_auc", "f1", "recall", "precision"]:
            row[f"cv_{metric}_mean"] = float(result[f"test_{metric}"].mean())
            row[f"cv_{metric}_std"] = float(result[f"test_{metric}"].std())
        rows.append(row)
    table = pd.DataFrame(rows).sort_values("cv_roc_auc_mean", ascending=False, kind="stable")
    # O critério combinado é ROC-AUC. F1 maior, sozinho, não muda esta escolha.
    winner = table.iloc[0]["model"]
    model = models[winner]
    with threadpool_limits(limits=1):
        model.fit(X_train, y_train)
    probability = model.predict_proba(X_test)[:, 1]
    metrics = evaluate(y_test, probability)
    groups = []
    for column in ["gender", "SeniorCitizen"]:
        for value in sorted(X_test[column].unique(), key=str):
            mask = (X_test[column] == value).to_numpy()
            groups.append({"feature": column, "group": str(value), "n": int(mask.sum()),
                **evaluate(y_test.to_numpy()[mask], probability[mask])})
    metadata = {"model_name": winner, "threshold": 0.5, "seed": SEED,
        "created_at": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
        "sklearn": sklearn.__version__, "train_rows": len(X_train), "test_rows": len(X_test),
        "dataset_sha256": hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
        "selection": "Maior ROC-AUC média em 5 folds somente no treino; limiar fixo 0.5",
        "features": FEATURES, "test_metrics": metrics}
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Salvamos o pipeline inteiro para a API repetir o tratamento do treinamento.
    joblib.dump({"pipeline": model, "metadata": metadata}, MODEL_PATH)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    table.to_csv(reports / "model_comparison.csv", index=False)
    (reports / "metrics.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    pd.DataFrame(groups).to_csv(reports / "subgroup_metrics.csv", index=False)
    print(table.to_string(index=False))
    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()
