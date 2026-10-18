# Experimentos da revisão

Esta revisão acrescenta perguntas e verificações ao projeto entregue. Não é uma reconstrução de etapas anteriores. As métricas originais do campeão continuam no Model Card.

## Pergunta 1: reduzir o limiar melhora tudo?

Notebook: `notebooks/02_erros_e_limiares.ipynb`.

O teste final original não foi usado nesta análise. Dos 5.634 registros de desenvolvimento, 4.225 foram usados para ajuste e 1.409 para validação interna. Seed 42, divisão estratificada e mesma configuração da Regressão Logística. O modelo da API não foi sobrescrito.

| Limiar | Precisão | Recall | F1 | Contatos | Falsos positivos | Falsos negativos |
|---|---:|---:|---:|---:|---:|---:|
| 0,3 | 41,995% | 91,176% | 0,5750 | 812 | 471 | 33 |
| 0,5 | 51,664% | 78,877% | 0,6243 | 571 | 276 | 79 |
| 0,7 | 63,295% | 58,556% | 0,6083 | 346 | 127 | 155 |

Baixar de 0,5 para 0,3 identificou 46 cancelamentos adicionais, mas acrescentou 195 falsos positivos e 241 contatos. A hipótese de que a precisão também melhoraria não se confirmou nesta divisão. ROC-AUC da validação interna: 0,8362.

**Decisão:** manter 0,5 no artefato atual. A análise não estabelece um limiar ótimo; faltam custos e capacidade da equipe de retenção. A configuração do candidato já era conhecida, portanto esta validação exploratória não constitui uma nova estimativa independente da seleção.

## Pergunta 2: onde se concentram os erros?

No limiar 0,5, por contrato:

| Contrato | Clientes | Cancelamentos | Falsos positivos | Falsos negativos |
|---|---:|---:|---:|---:|
| Month-to-month | 776 | 324 | 257 | 34 |
| One year | 308 | 37 | 19 | 32 |
| Two year | 325 | 13 | 0 | 13 |

O modelo deixou de identificar os 13 cancelamentos do grupo Two year nesta validação. Esse grupo tem poucos positivos; a taxa de falso negativo de 100% aqui não deve ser generalizada para outros dados. A tabela completa inclui denominadores e taxas, em `reports/review/errors_by_contract.csv`.

**Decisão:** documentar a limitação. Não remover o grupo ou mudar o modelo usando o teste final. Uma próxima investigação pode estudar mais divisões e a estabilidade desses resultados.

## Pergunta 3: entradas inválidas são tratadas claramente?

Notebook: `notebooks/03_cenarios_da_api.ipynb`.

Foram conferidos oito cenários: cliente válido; cobrança total omitida; tenure omitido; tenure negativo; contrato desconhecido; alvo enviado por engano; serviços incompatíveis; modelo ausente. Os status observados foram os esperados: 200, 422 ou 503. Respostas em `reports/review/api_scenarios.json`.

`/health` sem modelo informa `model_loaded: false` com status 200. Isso é uma verificação de processo, não de prontidão para inferência.

## Como reproduzir

No VS Code, selecione o Python da `.venv` nos notebooks 02 e 03 e use **Run All**. Alternativamente, na raiz:

```powershell
.\.venv\Scripts\python.exe scripts/run_review_notebooks.py
```

Se o ambiente bloquear sockets do Jupyter:

```powershell
.\.venv\Scripts\python.exe scripts/run_review_notebooks.py --in-process
```

A execução entregue foi feita com `--in-process`, pois o kernel Jupyter foi bloqueado pelo ambiente. As células foram executadas e suas saídas salvas; não foram inventadas saídas de execução. O script interrompe em caso de erro de célula. A alternativa padrão com kernel e a execução no Windows precisam ser conferidas no computador de destino.

Relatórios são sobrescritos ao executar novamente. Metadados de dados, versões e tamanhos estão em `reports/review/experiment_metadata.json`. As tabelas acima registram a execução incluída e devem ser revisadas se houver mudanças.
