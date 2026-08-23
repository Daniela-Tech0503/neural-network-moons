"""Possível solução pedagógica para NNPROJ-6."""
import numpy as np
import matplotlib.pyplot as plt

def plotar_fronteira(modelo, X, y, titulo="Fronteira de decisão"):
    margem = 0.5
    x_min, x_max = X[:, 0].min() - margem, X[:, 0].max() + margem
    y_min, y_max = X[:, 1].min() - margem, X[:, 1].max() + margem
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 300),
        np.linspace(y_min, y_max, 300),
    )
    pontos = np.c_[xx.ravel(), yy.ravel()]
    probabilidades = modelo.predict(pontos, verbose=0).reshape(xx.shape)
    plt.contourf(xx, yy, probabilidades, levels=20, cmap="RdBu_r", alpha=0.65)
    plt.contour(xx, yy, probabilidades, levels=[0.5], colors="black")
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr", edgecolor="white")
    plt.title(titulo)
    plt.colorbar(label="Probabilidade da classe 1")
    plt.show()
