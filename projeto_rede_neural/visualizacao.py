from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from contratos import ExecucaoExperiencia


def plotar_fronteira_decisao(
    execucao: ExecucaoExperiencia,
    caminho: Path,
) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    dados = execucao.dados
    X_original = np.vstack(
        [
            dados.scaler.inverse_transform(dados.X_treino),
            dados.scaler.inverse_transform(dados.X_teste),
        ]
    )
    y_original = np.concatenate([dados.y_treino, dados.y_teste])

    margem = 0.5
    passo = 0.02
    x_min, x_max = X_original[:, 0].min() - margem, X_original[:, 0].max() + margem
    y_min, y_max = X_original[:, 1].min() - margem, X_original[:, 1].max() + margem
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, passo),
        np.arange(y_min, y_max, passo),
    )
    grelha = np.c_[xx.ravel(), yy.ravel()]

    probabilidades = execucao.modelo.predict(
        dados.scaler.transform(grelha),
        verbose=0,
    ).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.contourf(xx, yy, probabilidades, cmap="RdBu", alpha=0.6, levels=20)
    ax.contour(xx, yy, probabilidades, levels=[0.5], colors="black", linewidths=2)

    for classe, cor, nome in [(0, "tab:blue", "Classe 0"), (1, "tab:red", "Classe 1")]:
        mascara = y_original == classe
        ax.scatter(
            X_original[mascara, 0],
            X_original[mascara, 1],
            c=cor,
            edgecolors="k",
            linewidths=0.5,
            s=30,
            label=nome,
        )

    config = execucao.config
    ax.set_title(f"{config.id_experiencia} - fronteira de decisao ({config.dataset})")
    ax.set_xlabel("Feature x1")
    ax.set_ylabel("Feature x2")
    ax.legend(loc="best")

    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plotar_curvas_loss(
    execucoes: list[ExecucaoExperiencia],
    caminho: Path,
) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    for execucao in execucoes:
        epocas = range(1, len(execucao.historico_loss) + 1)
        rotulo = f"{execucao.config.id_experiencia} ({execucao.config.ativacao})"
        ax.plot(epocas, execucao.historico_loss, label=rotulo, linewidth=2)

    ids = " vs ".join(e.config.id_experiencia for e in execucoes)
    ax.set_title(f"Curvas de loss de treino: {ids}")
    ax.set_xlabel("Epoca")
    ax.set_ylabel("Loss (binary_crossentropy)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
