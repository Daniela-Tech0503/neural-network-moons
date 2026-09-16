# Conclusão — Comparação E01 vs E05

**Responsável:** Helton Gomes Soares de Lima

## Resultados obtidos

| Experiência | Dataset | Parâmetros | Accuracy (teste) | Loss (teste) |
|---|---|---|---|---|
| E01 (baseline) | make_moons | 105 | 0,9040 | 0,2027 |
| E05 | make_circles | 105 | 0,9120 | 0,2277 |

## Conclusão

Executei a mesma arquitetura (2 camadas ocultas, 8 neurônios por camada, ativação tanh) sobre os dois datasets não lineares, mantendo fixos todos os demais parâmetros: seed 42, split 75/25 estratificado, normalização via StandardScaler ajustado apenas no treino, otimizador Adam, 100 épocas e batch size 16.

O número de parâmetros do modelo permaneceu idêntico (105) nas duas execuções, confirmando que a única variável alterada entre E01 e E05 foi, de fato, o dataset. Em termos de desempenho, a rede obteve accuracy ligeiramente superior em make_circles (91,2%) em relação a make_moons (90,4%), mas com uma loss de teste um pouco mais alta (0,2277 contra 0,2027).

A diferença entre os dois resultados é pequena e não permite concluir, com uma única execução, que a rede generaliza melhor para um formato de dado não linear do que para o outro. Como o projeto utiliza uma única seed, não é possível medir a variabilidade que existiria entre diferentes execuções da mesma configuração — uma diferença de menos de 1 ponto percentual de accuracy pode perfeitamente estar dentro da margem de aleatoriedade do treino, e não refletir uma vantagem real de uma base sobre a outra. O que se pode afirmar com segurança é que a mesma arquitetura simples foi capaz de aprender fronteiras de decisão razoáveis em ambos os formatos (meias-luas e círculos concêntricos), o que já demonstra a capacidade da rede de lidar com padrões não lineares distintos.
