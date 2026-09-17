# Conclusão — Task 1.1: Comparar Número de Neurônios (E01 vs E02)

**Responsável:** Luciana Almeida
**Reviewer:** Daniela Amaro

## Resultados obtidos

Pipeline comum, seed 42, make_moons (500 amostras, noise 0,15), 2 camadas ocultas,
ativação tanh, split 75/25 estratificado, StandardScaler ajustado só no treino,
Adam, 100 épocas, batch size 16. Única variável alterada: neurônios por camada.

| Experiência | Neurônios/camada | Parâmetros | Accuracy (teste) | Loss (teste) |
|---|---:|---:|---:|---:|
| E01 (baseline) | 8 | 105 | 0,9840 | 0,0853 |
| E02 | 16 | 337 | 0,9920 | 0,0278 |

## Conclusão

Dobrar os neurônios por camada (8 → 16) mais que triplicou o número de parâmetros
da rede (105 → 337, +221%), mas o ganho em accuracy foi pequeno (+0,8 ponto
percentual, de 98,40% para 99,20%). A loss de teste caiu mais — de 0,0853 para
0,0278 — o que indica que a rede maior não está apenas acertando mais casos, mas
fazendo isso com mais confiança (probabilidades mais próximas de 0 ou 1).

Isso é esperado: o make_moons com noise 0,15 é um problema relativamente simples
de separar, e a rede baseline (8 neurônios) já opera perto do teto de accuracy
possível para este nível de ruído. Aumentar a capacidade da rede reduz o erro
residual (loss), mas o retorno em accuracy é decrescente — sinal de que, para este
dataset, 8 neurônios por camada já é uma escolha de complexidade eficiente, e ir
para 16 só compensa se a métrica que importa for a confiança das previsões (loss),
não a taxa de acerto.
