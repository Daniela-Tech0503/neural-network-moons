"""Possível solução pedagógica para NNPROJ-11."""
from time import perf_counter
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def avaliar(nome, modelo, X_treino, y_treino, X_teste, y_teste):
    inicio = perf_counter()
    modelo.fit(X_treino, y_treino, epochs=100, batch_size=16, verbose=0)
    segundos = perf_counter() - inicio
    prob = modelo.predict(X_teste, verbose=0).ravel()
    prev = (prob >= 0.5).astype(int)
    return {
        "modelo": nome,
        "accuracy": accuracy_score(y_teste, prev),
        "precision": precision_score(y_teste, prev),
        "recall": recall_score(y_teste, prev),
        "f1": f1_score(y_teste, prev),
        "tempo_s": segundos,
    }

# resultados = [avaliar(...), avaliar(...)]
# pd.DataFrame(resultados).to_csv("benchmark.csv", index=False)
