# Conclusão — Task 2.1: Comparar Ativações Tanh e ReLU (E01 vs E04)

**Responsável:** Luciana Almeida
**Reviewer:** Daniela Amaro

## Resultados obtidos

Pipeline comum, seed 42, make_moons (500 amostras, noise 0,15), 2 camadas ocultas,
8 neurônios por camada, split 75/25 estratificado, StandardScaler ajustado só no
treino, Adam, 100 épocas, batch size 16. Única variável alterada: função de
ativação das camadas ocultas.

| Experiência | Ativação | Parâmetros | Accuracy (teste) | Loss (teste) |
|---|---|---:|---:|---:|
| E01 (baseline) | tanh | 105 | 0,9840 | 0,0853 |
| E04 | relu | 105 | 0,9440 | 0,1522 |

Curva de loss de treino (`curva_loss_e01_e04.png`), mesmos pontos das duas curvas:

| Época | E01 (tanh) | E04 (relu) |
|---:|---:|---:|
| 10 | 0,3650 | 0,4139 |
| 30 | 0,2807 | 0,2610 |
| 100 | 0,0912 | 0,1376 |

## Conclusão

O número de parâmetros é idêntico (105) nas duas experiências — trocar a ativação
não muda a capacidade nominal da rede, só a forma como ela aprende. Ainda assim, a
tanh superou a relu nesta configuração: +4,0 pontos percentuais de accuracy
(98,40% vs 94,40%) e menos da metade da loss de teste (0,0853 vs 0,1522).

A curva de treino mostra o porquê: até a época 30 as duas ativações estão
praticamente empatadas (E04 até um pouco à frente, 0,261 vs 0,281). A partir daí
elas divergem — a tanh continua caindo e termina em 0,091, enquanto a relu
desacelera e estagna em 0,138. Isto é consistente com o problema clássico da
ReLU em redes pequenas e rasas: como a ReLU zera qualquer entrada negativa, parte
dos neurônios pode ficar "presa" em zero de forma mais frequente do que com a
tanh (que é suave e centrada em zero, com gradiente não-nulo em toda a sua
faixa), reduzindo a capacidade efetiva da rede justamente quando ela mais precisa
refinar a fronteira de decisão entre as duas luas.

Para esta arquitetura pequena (2 camadas, 8 neurônios, 100 épocas), tanh é a
escolha mais eficaz; relu tende a compensar melhor em redes maiores/mais
profundas, fora do escopo desta task.
