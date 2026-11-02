# Como ler os testes

Arquivo: `tests/test_project.py`. A revisão contém **13 casos executados**: os seis originais e sete novos. Há dez funções de teste; uma é parametrizada e gera quatro casos.

## Preparação

A fixture `payload` abre um exemplo válido. A fixture `artifact` treina uma Regressão Logística temporária nos primeiros 400 registros e salva o pipeline em uma pasta temporária do pytest. Ela serve para verificar integração, não para medir desempenho preditivo ou substituir o campeão. `TestClient` chama a aplicação em processo, sem servidor HTTP aberto.

| Teste | O que verifica | Exemplo |
|---|---|---|
| test_cleaning_drops_target_and_id_without_mutating | Limpeza sem modificar a entrada e exclusão do alvo e ID | TotalCharges com espaço vira NaN |
| test_missing_column | Falta de coluna na função de preparação | Remover tenure causa ValueError |
| test_health_without_model | Estado informado pela API sem artefato | model_loaded é false |
| test_predict_unavailable | Inferência recusada sem modelo | /predict responde 503 |
| test_predict_pipeline_and_validation | Integração, faixa do score, classe e entradas inválidas | Score >= 0,5 deve produzir classe 1 |
| test_missing_total_charges_is_imputed | Integração aceita cobrança ausente | Omitir TotalCharges retorna 200 |
| test_imputer_uses_training_median | Estatísticas do imputador e valor efetivamente preenchido | A transformação deve preencher TotalCharges com a mediana do treino temporário |
| test_invalid_inputs_report_the_field (4 casos) | Status 422 e identificação do campo rejeitado | tenure, MonthlyCharges e TotalCharges negativos; Contract inexistente |
| test_missing_tenure_is_rejected_by_api | Coluna obrigatória também validada no contrato HTTP | Omitir tenure retorna 422 e localiza o campo |
| test_internet_services_must_be_consistent | Coerência entre internet e serviços dependentes | InternetService=No e OnlineSecurity=Yes retorna 422 |

## O que melhorou na revisão

O teste original de TotalCharges conferia apenas o status 200. O novo teste compara as estatísticas aprendidas pelo imputador com as medianas do treino e verifica o valor inserido antes da escala. Isso observa o comportamento numérico, além de verificar que a requisição terminou sem erro.

Os testes parametrizados conferem o campo informado no erro. Isso ajuda quem consome a API a localizar o dado incorreto, em vez de receber apenas um status genérico.

## Executar

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Resultado da revisão: **13 passed**. Houve um aviso de depreciação da integração de TestClient/Starlette com http no ambiente instalado. Ele não falhou os testes; está registrado em `reports/review/validation.txt`. Não foram alteradas as dependências para resolver esse aviso nesta revisão.

## Limites

Esta suíte não mede latência de rede, segurança de produção, qualidade do ranking ou ganho financeiro. As métricas de ML e os experimentos ficam nos relatórios e notebooks. Os oito cenários do notebook 03 são uma demonstração adicional.
