# Conclusão — Comparação E01 vs E05

**Responsável:** Helton Gomes Soares de Lima
**Revisão após o merge do PR #1:** Daniela Amaro (ver notas no fim)

## Resultados obtidos

Ambiente de referência: Python 3.13, TensorFlow 2.21 (CPU), seed 42, determinismo ativado.

| Experiência | Dataset | Parâmetros | Accuracy (teste) | Loss (teste) |
|---|---|---|---|---|
| E01 (baseline) | make_moons | 105 | 0,9840 | 0,0853 |
| E05 | make_circles | 105 | 0,6240 | 0,6668 |

## Conclusão

Executámos a mesma arquitetura (2 camadas ocultas, 8 neurónios por camada, ativação
tanh) sobre os dois datasets não lineares, mantendo fixos todos os demais parâmetros:
seed 42, split 75/25 estratificado, normalização via StandardScaler ajustado apenas no
treino, otimizador Adam, 100 épocas e batch size 16. O número de parâmetros permaneceu
idêntico (105), confirmando que a única variável alterada entre E01 e E05 foi o dataset.

O resultado mais importante desta comparação é a **grande diferença de dificuldade
entre as duas bases**. No make_moons, a mesma rede atinge 98,4% de accuracy. No
make_circles, fica-se pelos 62,4%, com loss de teste 0,667 — muito próxima de
ln(2) ≈ 0,693, que é a loss de um modelo que responde "50/50" para tudo.

A explicação é geométrica: com os parâmetros oficiais (noise 0,15 e o `factor`
padrão 0,8 do scikit-learn), os dois anéis do make_circles ficam nos raios médios
0,8 e 1,0 — um intervalo de apenas 0,2, da mesma ordem do ruído. As duas classes
sobrepõem-se fisicamente, pelo que **nem o melhor classificador possível acertaria
muito mais**. Testes de diagnóstico (fora do protocolo) com outras seeds deram
0,46–0,78, confirmando que não é um acaso da seed 42 nem um defeito do treino.

Conclusão proporcional à evidência: a arquitetura baseline aprende bem o formato
meias-luas e não consegue aprender o formato círculos **nesta configuração de
ruído e fator**. Isto ilustra que o desempenho de um modelo depende tanto do
problema (separabilidade dos dados) como da arquitetura — e que comparar
experiências entre datasets diferentes mede sobretudo a dificuldade de cada um.

## Notas da revisão (o que mudou face à versão original do PR #1)

1. A versão original do `dados.py` usava `factor=0.5` no `make_circles`, um valor
   fora do contrato que separa artificialmente os anéis e produzia E05 ≈ 0,912.
   Foi removido: o contrato não define `factor`, portanto usa-se o padrão (0,8),
   igual para toda a equipa. A conclusão anterior ("circles ligeiramente melhor
   que moons") invertia-se por causa deste parâmetro escondido.
2. Os valores de E01 também mudaram (0,9040 → 0,9840) porque o ambiente de
   referência passou de TensorFlow <2.17 para 2.21 e as seeds foram reforçadas
   (PYTHONHASHSEED, random, numpy, tf + determinismo). Versões diferentes de
   TensorFlow geram pesos iniciais diferentes para a mesma seed — daí a
   importância de a equipa usar o mesmo `requirements.txt`.
