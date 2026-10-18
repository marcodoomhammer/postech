"""Download explícito; verifica integridade antes de substituir o CSV."""
import hashlib
from urllib.request import urlopen
from churn.config import DATA_PATH
URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
EXPECTED = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
def main():
    with urlopen(URL, timeout=60) as response:
        content = response.read()
    if hashlib.sha256(content).hexdigest() != EXPECTED:
        raise ValueError("A fonte mudou. Revise os dados antes de atualizar o hash esperado.")
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_bytes(content)
    print(f"Dados salvos em {DATA_PATH}")
if __name__ == "__main__":
    main()
