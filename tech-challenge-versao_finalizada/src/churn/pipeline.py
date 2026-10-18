from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from .config import NUMERIC, CATEGORICAL, SEED

def build_pipeline(estimator):
    # Mediana e escala precisam ser aprendidas em cada fold, e não no CSV inteiro.
    # Por isso o tratamento fica junto do classificador no mesmo pipeline.
    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                            ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return Pipeline([("preprocess", ColumnTransformer([
        ("numeric", numeric, NUMERIC), ("categorical", categorical, CATEGORICAL)])),
        ("classifier", estimator)])

def candidates():
    # Estas configurações são o ponto de partida, não uma busca de parâmetros.
    # Mantemos a mesma seed para tornar a comparação mais fácil de reproduzir.
    return {
        "logistic_regression": build_pipeline(LogisticRegression(max_iter=1500, class_weight="balanced", random_state=SEED)),
        "random_forest": build_pipeline(RandomForestClassifier(n_estimators=200, max_depth=10,
            min_samples_leaf=4, class_weight="balanced", random_state=SEED, n_jobs=1)),
        "mlp": build_pipeline(MLPClassifier(hidden_layer_sizes=(32, 16), alpha=0.01,
            max_iter=500, early_stopping=True, n_iter_no_change=20, random_state=SEED)),
    }
