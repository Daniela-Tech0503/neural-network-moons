# Neural Network Moon Project

Pipeline de experiências controladas com uma rede neural (Keras/TensorFlow) para
classificação binária nos datasets `make_moons` e `make_circles`.

## O que é este projeto?

Cinco experiências (E01 a E05), cada uma alterando exatamente uma variável em
relação à baseline E01, com tudo o resto fixo: 500 amostras, noise 0.15, seed 42,
25% de teste, StandardScaler, Adam, binary_crossentropy, 100 épocas, batch size 16.

| ID | Dataset | Camadas ocultas | Neurónios | Ativação | Elemento estudado |
|---|---|---:|---:|---|---|
| E01 | make_moons | 2 | 8 | tanh | Baseline |
| E02 | make_moons | 2 | 16 | tanh | Número de neurónios |
| E03 | make_moons | 1 | 8 | tanh | Número de camadas |
| E04 | make_moons | 2 | 8 | relu | Função de ativação |
| E05 | make_circles | 2 | 8 | tanh | Base de dados |

Estado atual: Todas as experiências (E01 a E05), módulo de visualização
(`visualizacao.py`), fronteiras de decisão, curvas de loss e o Relatório Final em
PDF (`relatorio/relatorio_final.pdf`) estão 100% implementados e consolidados.

## Versão de Python

Testado com Python 3.13 e TensorFlow 2.21 (CPU). Versões diferentes de
TensorFlow podem produzir accuracy/loss ligeiramente diferentes mesmo com a
mesma seed — as conclusões qualitativas mantêm-se.

## Como criar e ativar o ambiente virtual

A partir da raiz do repositório:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Como instalar as dependências

```powershell
python -m pip install -r projeto_rede_neural\requirements.txt
```

## Como executar

Execução completa de todas as 5 experiências (gera o CSV e os 3 gráficos):

```powershell
cd projeto_rede_neural
python executar_experiencias.py
```

Testes mínimos de validação:

```powershell
cd projeto_rede_neural
python test_fundacao.py
```

Gerar / regenerar o Relatório Final em PDF:

```powershell
cd projeto_rede_neural\relatorio
python gerar_relatorio_final.py
```

## Ficheiros gerados

- CSV: `projeto_rede_neural/resultados/resultados.csv` (5 linhas, E01 a E05).
- Figuras:
  - `projeto_rede_neural/figuras/E01_fronteira_make_moons.png`
  - `projeto_rede_neural/figuras/E05_fronteira_make_circles.png`
  - `projeto_rede_neural/figuras/E01_E04_curvas_loss.png`
- Relatório: `projeto_rede_neural/relatorio/relatorio_final.pdf` (13 secções completas).

## Responsáveis

| Tarefa | Responsável |
|---|---|
| Pipeline comum, baseline E01, E05, consolidação CSV | Helton Gomes Soares de Lima |
| E02 (neurónios) e E04 (ativações) | Luciana Almeida |
| E03 (camadas), visualizações, relatório final | Pedro Rodrigues |
| Revisão geral | Daniela Amaro |
