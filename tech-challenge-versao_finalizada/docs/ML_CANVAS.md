# ML Canvas — Retenção de clientes de telecom

| Elemento | Definição |
|---|---|
| Problema | Priorizar clientes com maior risco de cancelamento para apoiar campanhas de retenção. |
| Stakeholders | Diretoria, CRM/marketing, atendimento, engenharia de dados, equipe de ML, jurídico e clientes. |
| Usuário | Analista de CRM consultando scores para montar uma campanha. |
| Decisão | Ordenar a base elegível pelo score; selecionar uma lista dentro da capacidade operacional. |
| Dados | Amostra pública IBM Telco; 7.043 clientes, 19 features, rótulo Churn e ID removido. |
| Rótulo | Churn=Yes indica saída no último mês; sem coorte temporal real disponível. |
| Entrada | Contrato, serviços, tempo de relacionamento e cobranças, observados antes da decisão em uso futuro. |
| Saída | Score entre 0 e 1 e classe pelo limiar acadêmico 0,5. |
| Métrica técnica | ROC-AUC média em CV para seleção; F1, recall, precisão e AP complementares. |
| Métrica operacional | Recall de churn na lista dos 20% maiores scores. |
| Meta proposta | Cobrir pelo menos 40% dos churners contatando 20% da base em avaliação offline. Meta acadêmica definida como referência; não validada com stakeholder real. |
| Métrica de negócio futura | Cancelamentos evitados e margem incremental líquida em experimento A/B, descontados contatos e incentivos. |
| Erros | Falso positivo gera contatos/custos desnecessários; falso negativo deixa churn sem ação. |
| Baseline | Regressão Logística com pesos balanceados e pipeline. |
| Alternativas | Random Forest e MLPClassifier; comparação com mesmos folds e features. |
| Restrições | Dados de demonstração; sem custos reais, datas de observação ou efeito de campanhas. |
| Implantação | API FastAPI local; nuvem opcional fora desta entrega. |
| Monitoramento proposto | Validação de schema, latência, taxa de erro, drift de entradas e performance por coorte/grupo após chegada dos rótulos. |
| Responsáveis | Preencher nomes e papéis em CONTRIBUTIONS.md. |

Não é possível inferir benefício causal ou financeiro apenas pelo score. Em produção, definir uma data de referência e horizonte futuro de cancelamento antes de coletar o dataset.
