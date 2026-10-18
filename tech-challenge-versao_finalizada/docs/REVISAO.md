# O que mudou nesta revisão

## Comentários e leitura

Os comentários em data.py, pipeline.py, train.py, schemas.py e api.py agora explicam motivos: por que não transformar cobrança ausente em zero; por que aprender estatísticas dentro do pipeline; por que rejeitar campos extras; e por que guardar o pré-processamento junto do modelo. Não foram inseridos erros artificiais ou atribuições de autoria.

O notebook 01 recebeu orientações de leitura. Suas saídas originais foram preservadas; os novos notebooks 02 e 03 foram executados nesta revisão.

## Adições

- `notebooks/02_erros_e_limiares.ipynb`: limiares 0,3/0,5/0,7, falsos positivos e negativos, análise por contrato.
- `notebooks/03_cenarios_da_api.ipynb`: oito cenários de sucesso ou erro esperado.
- `scripts/run_review_notebooks.py`: execução com kernel do mesmo Python ou alternativa explícita em processo.
- `docs/EXPERIMENTOS.md`: hipóteses, resultados medidos e limitações.
- `docs/GUIA_DOS_TESTES.md`: explicação dos 13 casos da suíte.
- `reports/review/`: tabelas, figura, metadados, respostas e resumo da validação.

O campeão, o dataset, o limiar da API e as métricas finais originais não foram alterados. Os resultados novos vêm de uma validação interna diferente, com o mesmo número de linhas do teste final por coincidência das proporções.

## Revisão pela equipe

1. Ler o notebook 02 e explicar o aumento de contatos ao reduzir o limiar.
2. Conferir a limitação observada para contratos de dois anos.
3. Executar os testes e o notebook 03 no Windows.
4. Preencher contribuições reais e adequar a declaração de assistência às regras da instituição.
5. Publicar apenas alterações efetivamente revisadas pela equipe.

Nenhum commit ou repositório remoto foi criado nesta revisão.
