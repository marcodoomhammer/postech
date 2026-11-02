# Dataset e proveniência

Fonte primária consultada: https://github.com/IBM/telco-customer-churn-on-icp4d
CSV: https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv
Download direto usado pelo script: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv
Consulta/download: 15/10/2026. Repositório de origem arquivado. A origem é um exemplo público da IBM, não dados operacionais próprios.

SHA-256: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`.

7.043 linhas; 21 colunas no original: customerID, 19 features, Churn. Clientes únicos; Churn Yes/No. Dataset original incluído no ZIP para execução offline. Mantida a atribuição; este projeto não redefine a licença dos dados. Antes de redistribuição pública, revise os termos do material original.

| Campos | Significado |
|------------------------------------------------------------------------------------------------------------------------------------|
| customerID | Identificador; excluído do modelo e da API |
| Churn | Alvo Yes/No; saída no último mês |
| gender, SeniorCitizen, Partner, Dependents | Características demográficas/familiares; SeniorCitizen 0/1 |
| tenure | Tempo de relacionamento em meses |
| PhoneService, MultipleLines | Telefonia e múltiplas linhas |
| InternetService | DSL, Fiber optic ou No |
| OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport | Serviços adicionais |
| StreamingTV, StreamingMovies | Serviços de streaming |
| Contract | Month-to-month, One year, Two year |
| PaperlessBilling, PaymentMethod | Cobrança e meio de pagamento |
| MonthlyCharges, TotalCharges | Cobrança mensal e acumulada, na unidade monetária original |

O contrato completo de campos/categorias da API está em `src/churn/schemas.py` e `/docs`. Valores monetários não são convertidos para reais. `TotalCharges` com espaços é convertido em NaN e imputado pela mediana aprendida no treino.

Referências técnicas:

 https://scikit-learn.org/stable/common_pitfalls.html ; 
 https://scikit-learn.org/stable/modules/cross_validation.html ; 
 https://fastapi.tiangolo.com/advanced/events/ ; 
 https://fastapi.tiangolo.com/advanced/testing-events/ .
