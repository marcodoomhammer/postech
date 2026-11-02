# Model Card — Telco Churn

## Identificação e uso

Campeão: **logistic_regression** (Scikit-Learn 1.8.0). Pipeline completo em `models/champion.joblib`. 

Demonstração acadêmica de classificação e priorização de retenção.

## Dados e protocolo

Fonte: CSV público de demonstração IBM Telco Customer Churn. 7043 registros, 1869 churners (26.54%). 19 features, incluindo gênero e indicador de idade sênior. ID excluído. Cobrança total contém 11 ausências após conversão numérica.

Treino/teste estratificados: 5634/1409. Cinco folds no treino; seleção por ROC-AUC média; limiar fixo 0,5. Pré-processamento ajustado dentro de cada fold, nunca no teste. Artefato ajustado apenas nos 80% de treino. Não houve busca exaustiva de hiperparâmetros ou ajuste de limiar.

## Comparação em CV (somente treino)

| Modelo              | ROC-AUC média ± desvio | F1 médio |
|------------------------------------------------------|
| logistic_regression | 0.8459 ± 0.0124        | 0.6279 |
| random_forest       | 0.8456 ± 0.0090        | 0.6333 |
| mlp                 | 0.8428 ± 0.0104        | 0.5838 |

Os desvios descrevem variação entre folds, não intervalos de confiança. Diferenças pequenas não demonstram superioridade estatística. A Regressão Logística ate o monento tem o melhor desenpnho critério pré-definido; sua simplicidade também facilita inspeção.

## Resultado do campeão no teste reservado

| Métrica                         | Resultado |
|------------------------------------------------------|
| ROC-AUC                         | 0.8413 |
| Average precision               | 0.6326 |
| F1 (limiar 0,5)                 | 0.6136 |
| Precisão                        | 0.5043 |
| Recall                          | 0.7834 |
| Acurácia                        | 0.7381 |
| Recall nos 20% maiores scores   | 49.73% |
| Precisão nos 20% maiores scores | 65.96% |

Matriz de confusão: TN=747, FP=288, FN=81, TP=293. A meta operacional acadêmica de cobertura >=40% em uma lista de 20% foi atingida offline (49.73%). Isso não representa churn evitado em campanha real.

## Inspeção descritiva por grupo (teste, limiar 0,5)

| Grupo | N | Recall | Precisão |
|---|---|---|---|
| gender=Female | 687 | 0.7772 | 0.5300 |
| gender=Male | 722 | 0.7901 | 0.4799 |
| SeniorCitizen=0 | 1187 | 0.7319 | 0.4720 |
| SeniorCitizen=1 | 222 | 0.9286 | 0.5948 |

Grupos têm tamanhos e taxas base diferentes. A inspeção não prova equidade; faltam intervalos de confiança, avaliação interseccional e revisão contextual. Gênero e SeniorCitizen podem introduzir tratamento desigual; mantidos aqui para estudar e documentar o risco, sujeitos à revisão antes de uso real.

## Limitações

- Amostra de demonstração, sem evidência de representatividade real.
- Snapshot sem datas individuais: split aleatório não demonstra generalização temporal nem garante ausência de vazamento temporal na origem.
- Não há efeito causal de retenção, receita preservada, horizonte prospectivo validado ou calibração formal do score. Pesos de classe também podem alterar a interpretação probabilística.
- Sensibilidade a drift; contratos e preços mudam. Necessário revalidar com dados recentes e rótulos confiáveis.
- Aproximadamente metade dos positivos classificados é falso positivo; 
- API local, sem autenticação.

## Reprodução

`python scripts/download_data.py`, `python -m churn.train` e `python -m pytest -q`. SHA-256 dos dados: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`. Versões em requirements e lock. Se houver novo treino, atualizar este documento com as métricas geradas.


