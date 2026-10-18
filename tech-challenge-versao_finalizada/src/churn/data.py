import pandas as pd
from .config import DATA_PATH, FEATURES, NUMERIC, CATEGORICAL

def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Conversão determinística, sem aprender estatísticas do conjunto."""
    missing = set(FEATURES) - set(frame.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")
    # Trabalhamos em uma cópia: quem chamou a função pode precisar do dado original.
    # A lista FEATURES também impede que Churn e customerID cheguem ao modelo.
    result = frame[FEATURES].copy()
    # No CSV, TotalCharges tem espaços em algumas linhas. Isso vira ausência,
    # não zero: zero seria uma cobrança conhecida e mudaria o significado do dado.
    for col in NUMERIC:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    for col in CATEGORICAL:
        result[col] = result[col].map(lambda v: v.strip() if isinstance(v, str) else v)
        result[col] = result[col].replace("", float("nan"))
    return result

def load_data(path=DATA_PATH):
    frame = pd.read_csv(path)
    if "Churn" not in frame or not frame["Churn"].isin(["Yes", "No"]).all():
        raise ValueError("Churn deve conter somente Yes/No, sem valores ausentes.")
    if "customerID" not in frame or frame["customerID"].isna().any() or frame["customerID"].duplicated().any():
        raise ValueError("customerID deve ser preenchido e único para evitar vazamento entre partições.")
    return prepare_features(frame), frame["Churn"].map({"No": 0, "Yes": 1})
