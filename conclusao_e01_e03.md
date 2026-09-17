# Conclusão — Task 1.2: Comparar Número de Camadas Ocultas (E01 vs E03)

**Responsável:** Pedro Rodrigues  
**Reviewer:** Daniela Amaro  

## Resultados obtidos

Pipeline comum, seed 42, make_moons (500 amostras, noise 0,15), 8 neurónios por camada,
ativação tanh, split 75/25 estratificado, StandardScaler ajustado apenas no treino,
Adam, 100 épocas, batch size 16. Única variável alterada: número de camadas ocultas.

| Experiência | Camadas ocultas | Parâmetros | Accuracy (teste) | Loss (teste) |
|---|---:|---:|---:|---:|
| E01 (baseline) | 2 | 105 | 0,9840 | 0,0853 |
| E03 | 1 | 33 | 0,8800 | 0,2299 |

## Conclusão

Reduzir a rede de 2 camadas ocultas para 1 camada reduziu os parâmetros em 68,6%
(de 105 para 33: `2×8+8 = 24` na camada oculta e `8×1+1 = 9` na saída), mas causou a
maior perda de desempenho observada no dataset make_moons: a accuracy caiu 10,4 pontos
percentuais (de 98,40% para 88,00%) e a loss de teste quase triplicou (de 0,0853 para 0,2299).

A explicação está na profundidade e na capacidade de representação não linear.
Embora o Teorema da Aproximação Universal garanta que uma única camada oculta é
teoricamente capaz de aproximar qualquer função contínua se tiver neurónios suficientes,
com apenas 8 neurónios uma única camada tem dificuldade em curvar a fronteira de decisão
no formato de duas meias-luas entrelaçadas. A segunda camada oculta permite compor as
transformações não lineares da primeira camada, gerando fronteiras mais ricas e
adaptadas à geometria das luas com relativamente poucos parâmetros adicionais (72 pesos/biases).

Conclusão proporcional: para o problema do make_moons com 8 neurónios por camada, a
arquitetura com 2 camadas ocultas é significativamente mais eficaz do que com 1 camada.
A profundidade foi determinante para a separação correta das classes.
