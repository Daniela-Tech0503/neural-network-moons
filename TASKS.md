# Checklist — Tasks do Helton (Neural Network Moon Project)

Marque cada item com `[x]` conforme for validando. Só peça revisão à Daniela depois de todos os itens de uma task estarem marcados.

---

## Task 3 — Pipeline comum e baseline reprodutível

**Executor:** Helton Gomes Soares de Lima | **Reviewer:** Daniela Amaro

### Configuração E01 (baseline)
- [ ] Dataset: make_moons, 500 amostras, noise 0.15
- [ ] Seed: 42
- [ ] Split: 75% treino / 25% teste, com estratificação (`stratify=y`)
- [ ] Normalização: StandardScaler ajustado **apenas** no treino (`fit_transform` só em X_treino, `transform` em X_teste)
- [ ] Camadas ocultas: 2
- [ ] Neurônios por camada: 8
- [ ] Ativação: tanh
- [ ] Saída: sigmoid
- [ ] Otimizador: Adam
- [ ] Loss: binary_crossentropy
- [ ] Épocas: 100
- [ ] Batch size: 16

### Critérios de aceite
- [ ] Execução é reprodutível (mesma seed → mesmo resultado)
- [ ] **Não existe fuga de dados** (scaler nunca "vê" o teste antes da hora)
- [ ] Accuracy, loss e número de parâmetros são registrados em `resultados.csv`
- [ ] A pipeline permite configurar dataset, camadas, neurônios e ativação (via `ConfiguracaoExperiencia`)
- [ ] A configuração E01 é reutilizável pelas demais tasks/colegas (Luciana e Pedro conseguem importar e usar)

### Fora do escopo (não fazer)
- [ ] Confirmei que NÃO otimizei hiperparâmetros
- [ ] Confirmei que NÃO comparei otimizadores diferentes

---

## Task 2 — Comparação entre bases (E01 vs E05)

**Executor:** Helton Gomes Soares de Lima | **Reviewer:** Daniela Amaro

### Experiências
- [ ] E01: make_moons, 500 amostras, noise 0.15
- [ ] E05: make_circles, 500 amostras, seed 42, **mesma arquitetura da baseline**

### Mantido constante entre E01 e E05
- [ ] Número de camadas
- [ ] Neurônios por camada
- [ ] Ativação
- [ ] Seed
- [ ] Split
- [ ] Normalização
- [ ] Otimizador
- [ ] Épocas
- [ ] Batch size

### Critérios de aceite
- [ ] E01 e E05 executadas com a pipeline comum (`executar_experiencia`)
- [ ] Accuracy e loss registrados em `resultados.csv`
- [ ] Dados/modelos disponíveis para os gráficos de fronteira (Pedro vai usar)
- [ ] Conclusão breve escrita comparando as duas bases (texto pronto para o relatório)

### Fora do escopo (não fazer)
- [ ] Confirmei que NÃO usei dataset real
- [ ] Confirmei que NÃO adicionei outras bases além de moons/circles

---

## Task 1 — Consolidação da tabela final (E01–E05)

**Executor:** Helton Gomes Soares de Lima | **Reviewer:** Daniela Amaro

### Experiências esperadas na tabela
- [ ] E01 — baseline (make_moons, 2 camadas, 8 neurônios, tanh)
- [ ] E02 — 16 neurônios por camada (recebida da Luciana)
- [ ] E03 — 1 camada oculta (recebida do Pedro)
- [ ] E04 — ativação ReLU (recebida da Luciana)
- [ ] E05 — make_circles (própria)

### Colunas obrigatórias no `resultados.csv`
- [ ] Experiência
- [ ] Dataset
- [ ] Número de camadas
- [ ] Neurônios por camada
- [ ] Ativação
- [ ] Número de parâmetros
- [ ] Accuracy
- [ ] Loss

### Critérios de aceite
- [ ] Uma **função comum** foi usada para treino e avaliação em todas as 5 experiências (nenhuma tem código de treino próprio/customizado)
- [ ] `resultados.csv` é gerado automaticamente (não editado à mão)
- [ ] Todas as experiências usam Adam, seed 42, mesmo split, 100 épocas, batch size 16
- [ ] A baseline E01 está claramente identificada na tabela
- [ ] A tabela pode ser usada diretamente no relatório do Pedro (sem edição manual)
- [ ] Sem linhas duplicadas, ordenado por id_experiencia

### Fora do escopo (não fazer)
- [ ] Confirmei que NÃO incluí precision, recall ou F1
- [ ] Confirmei que NÃO fiz comparação de tempo ou benchmark de otimizadores

---

## Antes de enviar para a Daniela

- [ ] Rodei `python executar_experiencias.py` do zero e funcionou sem erros
- [ ] Conferi que `X_treino.shape == (375, 2)` e `X_teste.shape == (125, 2)`
- [ ] `git push` feito na branch correta, PR aberto
- [ ] Mensagem do PR referencia os IDs das tasks (Task 1 / Task 2 / Task 3 ou NNPROJ-5/8/11)
