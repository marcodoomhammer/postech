# Tech Challenge — Pipeline Preditivo de Churn

Projeto acadêmico completo: EDA, baseline de Regressão Logística, Random Forest, MLPClassifier, validação cruzada, seleção do campeão, API REST e testes automatizados.

**Resultado da execução incluída:** campeão Regressão Logística; ROC-AUC de teste **0,8413**, F1 **0,6136**, recall **0,7834**. O CSV real de demonstração IBM tem 7.043 clientes. Esses resultados são offline; não comprovam redução de churn em produção.

## Instalar as dependências e rodar a API localmente

### 1. Pré-requisitos

- Python **3.12 ou 3.13 de 64 bits**, conforme `pyproject.toml`.
- VS Code com a extensão Python; para executar os notebooks, instale também a extensão Jupyter.
- Acesso à internet para instalar as dependências e, se necessário, baixar o dataset.

A execução original foi validada com Python 3.12 no Linux. Os comandos abaixo usam Python 3.13 no Windows. Ao mudar de ambiente ou versão das bibliotecas, treine novamente o modelo antes de iniciar a API.

### 2. Abrir a pasta correta

Extraia o ZIP ou clone o repositório. No VS Code, use **Arquivo > Abrir Pasta** e escolha a pasta que contém `pyproject.toml`, `requirements.txt`, `src/` e `docs/`.

Este é o **README principal**, que deve ficar na raiz. O arquivo `models/README.md` documenta apenas os artefatos do modelo.

Abra **Terminal > Novo Terminal** e execute os comandos seguintes no PowerShell, sempre a partir da raiz do projeto.

### 3. Criar o ambiente virtual

Confira a instalação do Python:

```powershell
py -3.13 --version
```

Crie um ambiente isolado para as dependências do projeto:

```powershell
py -3.13 -m venv .venv
```

Se estiver usando Python 3.12, substitua `py -3.13` por `py -3.12` nesses dois comandos. Os demais comandos permanecem iguais.

Usaremos o executável da `.venv` diretamente. Assim, não é necessário ativar o ambiente nem alterar a política de execução do PowerShell.

### 4. Instalar as dependências e o projeto

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

O comando `pip install -e .` instala o pacote local `churn` em modo editável e as dependências fixadas em `requirements.txt`, conforme a configuração de `pyproject.toml`. Não é necessário instalar cada biblioteca separadamente.

Para reproduzir de forma mais estrita o ambiente original de Python 3.12, existe a alternativa descrita na seção **Dependências e reprodução**, usando `requirements-lock.txt`.

### 5. Conferir os dados e treinar o modelo

Verifique se existe o arquivo `data/raw/telco.csv`. Ele acompanha o ZIP, mas é ignorado pelo Git. Se estiver ausente após clonar o repositório, baixe-o:

```powershell
.\.venv\Scripts\python.exe scripts/download_data.py
```

O script verifica o SHA-256 do conteúdo antes de salvar o dataset. Se a verificação falhar, revise a fonte; não desabilite essa validação para continuar.

Treine os modelos no ambiente instalado:

```powershell
.\.venv\Scripts\python.exe -m churn.train
```

Aguarde o término. O treinamento compara os modelos, seleciona o campeão e gera `models/champion.joblib`, além dos relatórios em `reports/`.

O arquivo `.joblib` contém o pipeline treinado e os metadados necessários à inferência. A API não treina o modelo ao iniciar. Mesmo que o ZIP já inclua o campeão, refazer o treinamento evita reutilizar um artefato gerado com versões diferentes das bibliotecas. Carregue somente arquivos joblib de origem confiável.

### 6. Executar os testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

O pytest executa os testes existentes em `tests/`. A revisão incluída registra 13 casos aprovados; confira o resultado da execução no seu ambiente.

### 7. Iniciar a API localmente

```powershell
.\.venv\Scripts\python.exe -m uvicorn churn.api:app --host 127.0.0.1 --port 8000 --reload
```

Mantenha esse terminal aberto. A opção `--reload` reinicia o servidor ao alterar o código e é destinada ao desenvolvimento local.

Abra no navegador:

- Swagger: http://127.0.0.1:8000/docs
- Verificação do serviço: http://127.0.0.1:8000/health

Com o modelo carregado, `/health` deve retornar:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

`status: "ok"` informa que o serviço está ativo. Para realizar previsões, confira também se `model_loaded` está como `true`.

### 8. Fazer uma previsão pelo Swagger

1. Acesse http://127.0.0.1:8000/docs.
2. Expanda **POST /predict** e clique em **Try it out**.
3. Substitua o corpo da requisição pelo conteúdo de `docs/example_customer.json`.
4. Clique em **Execute**.
5. Confira o código HTTP **200** e os campos da resposta.

Exemplo de resposta registrada na entrega original, para o cliente de exemplo:

```json
{
  "churn_probability": 0.8021375859868237,
  "churn_prediction": 1,
  "threshold": 0.5,
  "model_name": "logistic_regression"
}
```

O score e o modelo retornados podem variar após novo treinamento. `churn_prediction` igual a `1` indica score maior ou igual ao limiar; `0` indica score abaixo dele. O score não passou por calibração adicional e não deve ser interpretado como probabilidade exata de cancelamento.

Também é possível testar em **outro terminal PowerShell**, mantendo a API em execução:

```powershell
$cliente = Get-Content .\docs\example_customer.json -Raw
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType 'application/json' -Body $cliente
```

### 9. Encerrar ou reiniciar

Para encerrar o servidor, pressione **Ctrl+C** no terminal em que o Uvicorn está executando.

Após treinar novamente ou substituir `champion.joblib`, pare e inicie a API novamente para carregar o novo artefato.

### Problemas comuns

| Problema | Como resolver |
|---|---|
| `py` não reconhecido | Confira a instalação do Python e do launcher; feche e reabra o terminal após instalar. |
| Python 3.13 não encontrado | Se tiver Python 3.12, use `py -3.12` para criar a `.venv`. |
| `No module named churn` ou `uvicorn` | Na raiz, execute ` .\.venv\Scripts\python.exe -m pip install -e .` e use esse mesmo Python para iniciar a API. |
| Dataset ausente | Execute ` .\.venv\Scripts\python.exe scripts/download_data.py` antes do treinamento. |
| `model_loaded: false` ou HTTP 503 em `/predict` | Execute o treinamento e reinicie a API. Confira também se `CHURN_MODEL_PATH` foi configurada para outro caminho. |
| Erro ao carregar o joblib | Confirme as versões das dependências, treine novamente no ambiente atual e reinicie a API. |
| HTTP 422 | Confira os campos e categorias do JSON com `docs/example_customer.json` e com o contrato do Swagger. |
| Porta 8000 ocupada | Inicie com `--port 8001` e use `http://127.0.0.1:8001/docs`. |

## Selecionar o interpretador e depurar

**Ctrl+Shift+P > Python: Select Interpreter** > `.venv\Scripts\python.exe`. Em **Executar e Depurar**, selecione **API FastAPI** ou **Treinar modelos** e pressione F5. Para o notebook, abra `notebooks/01_eda_baseline.ipynb`, selecione o kernel da `.venv` e use **Run All**. Execute o treinamento antes da seção comparativa se os relatórios ainda não existirem. O ZIP já contém as saídas das células.

## Linux/macOS

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m pytest -q
.venv/bin/python -m churn.train
.venv/bin/python -m uvicorn churn.api:app --reload
```

## API

| Rota | Resultado |
|---|---|
| GET `/health` | HTTP 200: processo ativo; `model_loaded` informa disponibilidade para inferência |
| POST `/predict` | Score de churn, classe 0/1, limiar e nome do modelo |
| GET `/docs` | Swagger interativo |

Os nomes e categorias seguem o CSV original em inglês. Exemplo completo em `docs/example_customer.json`. `TotalCharges` pode ser nulo ou omitido; a mediana do treino será usada. Outros campos são obrigatórios. Categorias, números negativos e combinações de serviços incoerentes retornam HTTP 422. Sem modelo, `/predict` retorna HTTP 503. Um joblib corrompido causa falha explícita no startup. `/health` é liveness, não readiness.

Exemplo PowerShell (outro terminal, API em execução):

```powershell
$cliente = Get-Content .\docs\example_customer.json -Raw
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType 'application/json' -Body $cliente
```

`churn_probability` é um score estimado entre 0 e 1, sem calibração adicional. `churn_prediction=1` significa score >= 0,5; não significa certeza de cancelamento. A configuração opcional `CHURN_MODEL_PATH` permite escolher outro artefato local confiável antes de iniciar a API.

## Método de avaliação

- Seed 42; split estratificado 80% treino e 20% teste (5.634 / 1.409 clientes).
- ID e alvo removidos das features. `TotalCharges` vazio vira ausente.
- Mediana numérica, moda categórica, StandardScaler e OneHotEncoder dentro do pipeline, reaprendidos em cada fold. O encoder tolera categorias desconhecidas; a API restringe as categorias ao contrato documentado.
- Cinco folds estratificados somente no treino, idênticos para os três modelos. Seleção pela maior ROC-AUC média. Limiar 0,5 fixado antes da avaliação.
- Regressão Logística e Random Forest com pesos balanceados; MLP com camadas (32,16), regularização e early stopping. O limite de 500 épocas vale para a MLP. Todos os parâmetros estão em `src/churn/pipeline.py`.
- Só o campeão escolhido em CV é ajustado no treino completo e avaliado no teste reservado. O artefato entregue é esse mesmo modelo, sem retreino no teste.
- Métrica de negócio operacional: recall de churn entre os 20% de maiores scores. A métrica é uma proxy de cobertura de campanha, não economia financeira demonstrada.
- A pequena diferença entre Logística e Random Forest não demonstra superioridade estatística. Veja dispersão em `reports/model_comparison.csv`.

## Estrutura

```text
src/churn/       configuração, dados, pipelines, treino, schemas, API
notebooks/       EDA, baseline, análise de erros e cenários da API
models/          campeão + metadados no joblib
reports/         métricas, comparação, análise por grupo, figuras e validação
data/raw/       CSV original (incluído no ZIP)
tests/           13 casos de limpeza, API, validação e imputação
scripts/         download verificável do dataset
docs/           ML Canvas, Model Card, STAR, dados e checklist
.vscode/         interpretador, extensões e depuração
.github/         workflow de testes para GitHub Actions
```

## Dependências e reprodução

A API foi validada com TestClient/ASGI em processo; o servidor TCP e a abertura do Swagger no navegador devem ser conferidos no seu Windows. Evidências em `reports/api_smoke_test.json` e `reports/test_results.txt`. O notebook foi executado célula a célula em processo porque o ambiente de validação restringe sockets de kernels Jupyter.

`requirements.txt` fixa versões diretas; `requirements-lock.txt` fixa também a árvore de dependências instalada na validação. Instalação mais estrita: instale `requirements-lock.txt` e depois o pacote com `pip install -e . --no-deps`. Não há lock de hashes de wheels. Pequenas diferenças numéricas entre sistemas e bibliotecas BLAS são possíveis apesar da seed. Testes usam um artefato temporário próprio. Carregue somente arquivos joblib confiáveis: a desserialização pode executar código.

## Repositório GitHub e trabalho em grupo

O ZIP contém os arquivos; **nenhum repositório remoto foi criado**. Crie um repositório vazio no GitHub. No terminal da pasta:

```bash
git init
git add .
git commit -m "Estrutura inicial do pipeline de churn"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/churn-tech-challenge.git
git push -u origin main
```

Substitua a URL pela sua. CSV e joblib são ignorados no Git; após clonar, instale o pacote, rode `python scripts/download_data.py`, depois `python -m churn.train`. Se quiser incluí-los conscientemente no repositório, revise origem, tamanho e autorização de redistribuição primeiro. O CI baixa o CSV com verificação SHA-256 e executa pytest.

O histórico de trabalho deve refletir contribuições reais. Esta entrega não fabrica commits nem autoria. Registre no `docs/CONTRIBUTIONS.md` quem revisou e implementou cada parte. Os integrantes devem compreender, revisar e adaptar o projeto às regras da instituição.

## Entrega

- `docs/ML_CANVAS.md`: problema, stakeholders, objetivos e métricas.
- `docs/MODEL_CARD.md`: performance real, limitações, uso e riscos.
- `docs/VIDEO_STAR.md`: roteiro com tempos para até cinco minutos.
- `docs/CHECKLIST.md`: conferência final e itens ainda humanos.
- `docs/DATASET.md`: fonte, integridade e dicionário resumido.

Grave o vídeo mostrando notebook, comparação, testes e chamada à API. Preencha integrantes, turma e links. Deploy em nuvem é opcional e não está incluído nesta versão local.


## Revisão: experimentos e testes adicionais

Esta versão inclui comentários sobre as decisões do código, dois notebooks novos executados e **13 casos pytest aprovados**. O campeão e suas métricas finais continuam os mesmos.

| Material | Como usar |
|---|---|
| `notebooks/02_erros_e_limiares.ipynb` | Investigar recall, precisão, contatos e erros por contrato, em validação interna |
| `notebooks/03_cenarios_da_api.ipynb` | Conferir oito cenários controlados com TestClient |
| `docs/EXPERIMENTOS.md` | Ler hipóteses, resultados medidos e limitações |
| `docs/GUIA_DOS_TESTES.md` | Entender cada um dos 13 casos pytest |
| `docs/REVISAO.md` | Conferir as alterações e o roteiro de revisão da equipe |

Para executar os novos notebooks pelo terminal:

```powershell
.\.venv\Scripts\python.exe scripts/run_review_notebooks.py
```

Se o ambiente bloquear sockets de kernels, use `--in-process`. As saídas desta entrega foram produzidas nessa modalidade. Os notebooks também podem ser abertos no VS Code e executados com **Run All** no kernel da `.venv`.

Na validação interna, baixar o limiar de 0,5 para 0,3 elevou o recall de 78,88% para 91,18%, mas reduziu a precisão de 51,66% para 42,00% e aumentou os contatos de 571 para 812. Essa análise não escolheu novo limiar e não usou o teste final.

Evidências da revisão: `reports/review/validation.txt`, tabelas CSV, figura e respostas JSON. O relatório original de seis testes em `reports/test_results.txt` foi mantido como registro da primeira entrega. Houve um aviso de depreciação de TestClient/Starlette com httpx, sem falhas de teste. A execução no Windows e o modo com kernel Jupyter devem ser conferidos no computador de destino.

