from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[2]
SEED = 42
DATA_PATH = ROOT / "data/raw/telco.csv"
MODEL_PATH = Path(os.environ.get("CHURN_MODEL_PATH", ROOT / "models/champion.joblib"))
NUMERIC = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL = ["gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
               "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
               "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
               "PaperlessBilling", "PaymentMethod"]
FEATURES = NUMERIC + CATEGORICAL
