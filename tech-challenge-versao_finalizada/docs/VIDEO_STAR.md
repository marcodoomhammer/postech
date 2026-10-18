# Roteiro STAR — duração alvo 4min45s

Ensaiar e ajustar a fala para não ultrapassar cinco minutos. Usar os resultados reais de reports; este roteiro corresponde à execução incluída. Abrir notebook, terminal e Swagger antes de gravar. Não gastar o tempo do vídeo instalando dependências ou aguardando o treinamento.

## 0:00–0:40 — Situation

Mostrar título e distribuição do churn no notebook.

“Uma operadora precisa priorizar clientes para ações de retenção. Trabalhamos com a amostra pública Telco Customer Churn da IBM, com 7.043 clientes e informações sobre contratos, serviços e cobranças. O alvo indica cancelamento no último mês. É uma amostra de demonstração, por isso os resultados não comprovam desempenho futuro em uma operadora real.”

## 0:40–1:10 — Task

Mostrar ML Canvas e estrutura de pastas.

“Nosso objetivo foi construir um fluxo reproduzível, da exploração até uma API REST. Definimos ROC-AUC como critério de seleção, acompanhando F1, precisão e recall. Como indicador operacional, medimos quantos cancelamentos aparecem na lista dos 20% de maiores scores.”

## 1:10–2:45 — Action

Mostrar notebook, pipeline.py e tabela comparativa.

“Separamos 20% dos clientes para teste final e mantivemos a seed 42. Retiramos o identificador, convertemos cobranças totais vazias para valores ausentes e colocamos imputação, padronização e codificação categórica dentro do pipeline. Assim, cada fold aprende o pré-processamento apenas no seu treino.

Comparamos Regressão Logística, Random Forest e uma rede neural MLP com duas camadas ocultas, usando cinco folds estratificados e os mesmos dados. Escolhemos o maior ROC-AUC médio, sem consultar o teste. A Regressão Logística teve 0,8460; a Random Forest 0,8456; e a MLP 0,8428. A diferença pequena não demonstra superioridade estatística. O modelo linear ficou como campeão pelo critério definido.

Organizamos o código produtivo em src e separamos a experimentação no notebook. Salvamos o pipeline completo, incluindo pré-processamento, para que a API use exatamente as mesmas transformações.”

## 2:45–4:10 — Result e demonstração

Executar `python -m pytest -q`; mostrar 13 casos aprovados. No Swagger executar GET /health e POST /predict com docs/example_customer.json. Mostrar retorno real.

“No teste reservado, o campeão atingiu ROC-AUC de 0,8413, F1 de 0,6136 e recall de 78,34%, com limiar 0,5. Na lista dos 20% de maiores scores, encontramos 49,73% dos cancelamentos observados. Isso mede cobertura offline, não cancelamentos efetivamente evitados.

Aqui estão os testes passando. A API informa sua disponibilidade em health e recebe os dados de um cliente em predict. A resposta traz o score, a classe, o limiar e o modelo utilizado. Entradas inválidas são rejeitadas com status 422.”

## 4:10–4:45 — Limitações e fechamento

Mostrar Model Card e README.

“Documentamos limitações, diferenças por grupo e o risco de aplicar dados de demonstração a uma população atual. O score não passou por calibração adicional. Para uso real, precisamos de avaliação temporal, auditoria de vieses, custos definidos com o negócio e experimento A/B de retenção. O repositório contém instruções para reproduzir o treino e executar a API.”

Inserir identificação dos integrantes e link do repositório na descrição do vídeo. Dividir a apresentação de acordo com contribuições reais. Gravar e publicar o vídeo é uma etapa humana ainda pendente.
