# Plano — Guia pedagógico do projeto de rede neural

## Objetivo
Criar um PDF em português, acessível a uma aluna iniciante, contendo:
- explicação detalhada do `exemplo4.py`;
- tradução dos termos técnicos para linguagem simples;
- imagens produzidas a partir dos dados e do treino;
- exemplos de aplicações reais equivalentes ao problema de classificação;
- explicação das 9 tarefas do Jira NNPROJ;
- possíveis soluções, com código comentado e explicação, apresentadas como alternativas pedagógicas e não como única resposta.

## Abordagem
1. Executar uma versão reproduzível da experiência `make_moons` e produzir gráficos.
2. Criar diagramas explicativos da arquitetura e da passagem da informação.
3. Redigir o guia por secções, começando pela intuição e depois mostrando a matemática/código.
4. Incluir soluções exemplificativas para cada tarefa Jira, mantendo-as separadas do código original.
5. Gerar o PDF com ReportLab.
6. Verificar abertura, número de páginas, conteúdo extraído e renderização visual.

## Artefactos
- `guia_rede_neural/figuras/*.png`
- `guia_rede_neural/solucoes_exemplo/*.py`
- `Guia_Projeto_Rede_Neural.pdf`

## Validação
- executar os scripts de dados/gráficos;
- compilar sintaticamente os exemplos;
- abrir o PDF com pypdf;
- extrair texto e confirmar secções essenciais;
- renderizar páginas para PNG e inspecionar visualmente uma amostra.

## Observação pedagógica
Os códigos de solução são modelos possíveis para estudo. O grupo deve compreendê-los, adaptá-los e justificar as decisões no trabalho, em vez de os copiar sem análise.